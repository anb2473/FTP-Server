from ....exception import ResourceIsDirectoryException, EndpointNotFoundException
from .processor import FileProcessor

class TxtProcessor(FileProcessor):
    def __init__(self, path):
        super().__init__(path)

    def process(self):
        if not self.path.exists():
            raise EndpointNotFoundException("Cannot GET nonexistent endpoint", self.path)

        if not self.path.is_file():
            raise ResourceIsDirectoryException("Cannot GET directory as \".txt\"", self.path)
        return self.path.read_text(encoding="utf-8")
