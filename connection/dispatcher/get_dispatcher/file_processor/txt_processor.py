from .file_processor import FileProcessor

class TxtProcessor(FileProcessor):
    def __init__(self, path):
        super().__init__(path)

    def process(self):
        return self.path.read_text(encoding="utf-8")
