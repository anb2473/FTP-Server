from .persister import Persister
import json
from ...hasher.txt_hasher import TxtHasher

class TxtPersister(Persister):
    def __init__(self, path):
        super().__init__(path)

    def push(self, content):
        self.path.write_text(content, encoding="utf-8")
        
        metadata_path = self.path.with_name(self.path.name + ".meta")
        metadata = []
        if metadata_path.exists():
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

        assert type(metadata) is list
        
        hasher = TxtHasher(self.path)
        hash = hasher.hash()
        metadata.append(hash)

        metadata_path.write_text(json.dumps(metadata), encoding="utf-8")

        return 0 
