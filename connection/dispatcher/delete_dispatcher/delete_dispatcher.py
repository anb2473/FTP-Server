from ..dispatcher import Dispatcher
from .file_processor.txt_processor import TxtProcessor
from .file_processor.file_processor import FileProcessor
from pathlib import Path
from ...exception import BadRequestException, FileProcessorNotFoundException

class DeleteDispatcher(Dispatcher):
    def __init__(self, root_path):
        super().__init__(root_path)
        self.file_processor_registry = {
                ".txt": TxtProcessor
                }

    def delete_path(self, absolute_path):
        suffix = absolute_path.suffix
        file_processor = self.file_processor_registry.get(suffix)
        if not file_processor:
            raise FileProcessorNotFoundException("Failed to load file processor - unsupported filetype", suffix)
      
        assert issubclass(file_processor, FileProcessor)
        instance = file_processor(absolute_path)

        status = instance.process()
        return status

    def execute(self, body, res):
        rel_endpoint = body.get("rel_endpoint")
        if not rel_endpoint:
            raise BadRequestException("DELETE request without relative endpoint (must include \"rel_endpoint\")")

        # Guard clauses to validate path directly in processor
        absolute_path = self.root_path / Path(rel_endpoint)

        status = self.delete_path(absolute_path)
        return res.status(status.code, status.message)
