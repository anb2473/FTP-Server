from pathlib import Path
import json

from .file_processor.dir_processor import DirProcessor
from ..dispatcher import Dispatcher
from .file_processor.file_processor import FileProcessor
from .file_processor.txt_processor import TxtProcessor
from ...exception import BadRequestException, FileProcessorNotFoundException

class GetDispatcher(Dispatcher):
    def __init__(self, root_path):
        super().__init__(root_path)
        self.file_processor_registry = {
                ".txt": TxtProcessor,
                "": DirProcessor
            }

    def read_metadata(self, absolute_path):
        metadata_path = absolute_path.with_name(absolute_path.name + ".meta")
        # metadata will be autocreated when a PUSH request is sent
        # as such metadata not found case can be ignored
        if not metadata_path.exists() or not metadata_path.is_file():
            return {} 
        metadata = metadata_path.read_text(encoding="utf-8")
        return json.loads(metadata)

    def read_path(self, absolute_path, rel_endpoint):
        suffix = absolute_path.suffix
        file_processor = self.file_processor_registry.get(suffix)
        if not file_processor:
            raise FileProcessorNotFoundException("Failed to load file processor - unsupported filetype", suffix)
      
        assert issubclass(file_processor, FileProcessor)
        instance = file_processor(absolute_path, rel_endpoint, self.root_path)

        content = instance.process()
        return content

    def execute(self, body, res):
        rel_endpoint = body.get("rel_endpoint")        
        if not rel_endpoint:
            raise BadRequestException("GET request without endpoint")
        
        absolute_path = self.root_path / Path(rel_endpoint)

        metadata = self.read_metadata(absolute_path)

        content = self.read_path(absolute_path, rel_endpoint)

        return res.status(40, {
            "content": content, 
            "metadata": metadata
        })
