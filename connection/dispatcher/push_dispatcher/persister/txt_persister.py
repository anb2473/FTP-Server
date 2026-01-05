from connection.exception import EndpointNotFoundException, ResourceIsDirectoryException
from .persister import Persister
from ....status import StatusPushSuccessful
import json
from ...hasher.txt_hasher import TxtHasher

class TxtPersister(Persister):
    def __init__(self, path, rel_endpoint, root_path):
        super().__init__(path, rel_endpoint, root_path)

    def push(self, content):
        self.path.write_text(content, encoding="utf-8")
        
        metadata_path = self.path.with_name(self.path.name + ".meta")
        metadata = []
        if metadata_path.exists() or metadata_path.is_file():
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

        assert type(metadata) is list
        
        hasher = TxtHasher(self.path, self.rel_endpoint, self.root_path)
        hash = hasher.hash()
        metadata.append(hash)

        metadata_path.write_text(json.dumps(metadata), encoding="utf-8")

        return StatusPushSuccessful() 
