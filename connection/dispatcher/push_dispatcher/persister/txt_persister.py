from .persister import Persister

class TxtPersister(Persister):
    def __init__(self, path):
        super().__init__(path)

    def push(self, content):
        self.path.write_text(content, encoding="utf-8")
        return 0 
