from connection.exception import EndpointNotFoundException, ResourceIsDirectoryException
from connection.status import StatusDeleteSuccessful
from .file_processor import FileProcessor

class TxtProcessor(FileProcessor):
    def __init__(self, path, rel_endpoint, root_path):
        super().__init__(path, rel_endpoint, root_path)

    def process(self):
        if not self.path.exists():
            raise EndpointNotFoundException("Endpoint not found in DELETE request", self.path, self.rel_endpoint, self.root_path)
        if not self.path.is_file():
            raise ResourceIsDirectoryException("Cannot DELETE directory", self.path)

        self.path.unlink()
        return StatusDeleteSuccessful()
