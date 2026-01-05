from ....exception import ResourceIsDirectoryException, EndpointNotFoundException
from .file_processor import FileProcessor

class TxtProcessor(FileProcessor):
    def __init__(self, path, rel_endpoint, root_path):
        super().__init__(path, rel_endpoint, root_path)

    def process(self):
        if not self.path.exists():
            raise EndpointNotFoundException("Cannot GET nonexistent endpoint", self.path, self.rel_endpoint, self.root_path)
        if not self.path.is_file():
            raise ResourceIsDirectoryException("Cannot GET directory as \".txt\"", self.path)

        return self.path.read_text(encoding="utf-8")
