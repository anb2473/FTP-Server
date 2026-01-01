from connection.exception import EndpointNotFoundException, ResourceIsDirectoryException
from .persister import Persister
from ....status import StatusPushSuccessful
import json
from ...hasher.txt_hasher import TxtHasher

class TxtPersister(Persister):
    def __init__(self, path):
        super().__init__(path)

    def push(self, content):
        if not self.path.exists():
            raise EndpointNotFoundException("Cannot GET nonexistent endpoint", self.path)

        if not self.path.is_file():
            raise ResourceIsDirectoryException("Cannot GET directory as \".txt\"", self.path)

        self.path.write_text(content, encoding="utf-8")
        
        metadata_path = self.path.with_name(self.path.name + ".meta")
        metadata = []
        if metadata_path.exists() or metadata_path.is_file():
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

        assert type(metadata) is list
        
        hasher = TxtHasher(self.path)
        hash = hasher.hash()
        metadata.append(hash)

        metadata_path.write_text(json.dumps(metadata), encoding="utf-8")

        return StatusPushSuccessful() 
