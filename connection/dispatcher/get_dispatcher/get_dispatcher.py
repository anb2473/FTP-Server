from pathlib import Path
from ..dispatcher import Dispatcher
from .file_processor.file_processor import FileProcessor
from .file_processor.txt_processor import TxtProcessor

class BadRequestException(Exception):
    def __init__(self, message):
        super().__init__(message)

class FileProcessorNotFoundException(Exception):
    def __init__(self, message, suffix):
        super().__init__(message)
        self.suffix = suffix

class EndpointNotFoundException(Exception):
    def __init__(self, message, endpoint):
        super().__init__(message)
        self.rel_endpoint = endpoint

class GetDispatcher(Dispatcher):
    def __init__(self, root_path):
        super().__init__(root_path)
        self.file_processor_registry = {
                "txt": TxtProcessor
            }

    def execute(self, body, res):
        rel_endpoint = body.get("rel_endpoint")        
        if not rel_endpoint:
            raise BadRequestException("Fetch request without endpoint")
        
        absolute_path = self.root_path / Path(rel_endpoint)
        if not absolute_path.exists():
            raise EndpointNotFoundException("Failed to fetch endpoint in root", absolute_path)

        suffix = absolute_path.suffix
        file_processor = self.file_processor_registry.get(suffix)
        if not file_processor:
            raise FileProcessorNotFoundException("Failed to load file processor - unsupported filetype", suffix)
      
        assert issubclass(file_processor, FileProcessor)
        instance = file_processor(absolute_path)

        return res.status(0, instance.process()) 
