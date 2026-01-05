from connection.dispatcher.dispatcher import Dispatcher
from ..hasher.txt_hasher import TxtHasher
from ..hasher.hasher import Hasher
from ...exception import FileProcessorNotFoundException

class FetchDispatcher(Dispatcher):
    def __init__(self, root_path):
        self.root_path = root_path

        self.hasher_registry = {
                ".txt": TxtHasher
            }
    
    def load_dir(self, contents):
        loaded = {}
        for path in contents:
            if path.is_file():
                suffix = path.suffix
                if suffix == ".meta":
                    continue
                hasher = self.hasher_registry.get(suffix)
                if not hasher:
                    raise FileProcessorNotFoundException("Failed to load hasher - unsupported filetype", suffix)
             
                assert issubclass(hasher, Hasher)
                instance = hasher(path, path, self.root_path)
        
                stored_hash = instance.hash()
                loaded[path.name] = stored_hash
            elif not path.is_file():
                subdir_contents = path.iterdir()
                loaded[path.name] = self.load_dir(subdir_contents)
        return loaded

    def execute(self, body, res):
        contents = self.root_path.iterdir()
        return res.status(0, self.load_dir(contents))
