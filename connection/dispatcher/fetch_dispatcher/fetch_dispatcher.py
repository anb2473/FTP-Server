from connection.dispatcher.dispatcher import Dispatcher


class FetchDispatcher(Dispatcher):
    def __init__(self, root_path):
        self.root_path = root_path

    def load_dir(self, contents):
        loaded = {}
        for path in contents:
            if path.is_file():
                metadata_path = path.with_name(path.name + ".meta")

                metadata = {}
                # metadata automatically created on PUSH request
                # as such metadata not found case can be ignored
                if not metadata_path.exists() or not metadata_path.is_file():
                    metadata = metadata_path.read_text(encoding="utf-8")

                loaded[path.name] = metadata
            elif not path.is_file():
                subdir_contents = path.iterdir()
                loaded[path.name] = self.load_dir(subdir_contents)

    def execute(self, body, res):
        contents = self.root_path.iterdir()
        return res.status(0, self.load_dir(contents))
