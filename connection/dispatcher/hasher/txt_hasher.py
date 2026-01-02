from .hasher import Hasher
import hashlib

class TxtHasher(Hasher):
    def __init__(self, path):
        super().__init__(path)
        
    def hash(self) -> str:
        with self.path.open("rb") as f:
            digest = hashlib.file_digest(f, "sha256")
            return digest.hexdigest()
