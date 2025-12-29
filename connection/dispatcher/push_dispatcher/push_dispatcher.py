from ..dispatcher import Dispatcher
from .persister.txt_persister import TxtPersister
from .persister.persister import Persister
from pathlib import Path

class BadRequestException(Exception):
    def __init__(self, message):
        super().__init__(message)

class PersisterNotFoundException(Exception):
    def __init__(self, message, suffix):
        super().__init__(message)
        self.suffix = suffix

class PushDispatcher(Dispatcher):
    def __init__(self, root_path):
        super().__init__(root_path)
        self.persister_registry = {
                ".txt": TxtPersister
            }

    def execute(self, body, res):
        push_endpoint = body.get("push_endpoint")
        if not push_endpoint:
            raise BadRequestException("Push request without endpoint")

        rel_path = Path(push_endpoint)
        suffix = rel_path.suffix
        
        content = body.get("content")
        if not content:
            raise BadRequestException("Push request without content")

        absolute_path = self.root_path / rel_path
        
        persister = self.persister_registry.get(suffix)
        if not persister:
            raise PersisterNotFoundException("Persister not found in registry - unsupported filetype", suffix)

        assert issubclass(persister, Persister)
        instance = persister(absolute_path)

        ret_code = instance.push(content)
        if ret_code == 0:
            return res.status(ret_code, "Push successful")
        return res.status(ret_code, "Push failed")
