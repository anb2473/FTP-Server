from connection.exception import EndpointNotFoundException, ResourceIsFileException
from .file_processor import FileProcessor

class DirProcessor(FileProcessor):
    def __init__(self, path, rel_endpoint, root_path):
        super().__init__(path, rel_endpoint, root_path)

    def process(self):
        if not self.path.exists():
            raise EndpointNotFoundException("Cannot GET nonexistent endpoint", self.path, self.rel_endpoint, self.root_path)
        if self.path.is_file():
            raise ResourceIsFileException("Cannot GET file as directory", self.path)

        contents = self.path.iterdir()
        return str(list(contents))
