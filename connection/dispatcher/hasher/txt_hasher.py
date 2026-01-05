from .hasher import Hasher
import hashlib
from ...exception import EndpointNotFoundException, ResourceIsDirectoryException

class TxtHasher(Hasher):
    def __init__(self, path, rel_endpoint, root_path):
        super().__init__(path, rel_endpoint, root_path)
        
    def hash(self) -> str:
        if not self.path.exists(): 
            raise EndpointNotFoundException("Failed to compare nonexistent endpoints", self.path, self.rel_endpoint, self.root_path)
        if not self.path.is_file():
            raise ResourceIsDirectoryException("Cannot compare directories", self.path)

        with self.path.open("rb") as f:
            digest = hashlib.file_digest(f, "sha256")
            return digest.hexdigest()
