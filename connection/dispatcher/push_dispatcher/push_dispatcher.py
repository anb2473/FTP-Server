import json
from ..dispatcher import Dispatcher
from .persister.txt_persister import TxtPersister
from .persister.persister import Persister
from pathlib import Path
from ...exception import BadRequestException, PersisterNotFoundException

class PushDispatcher(Dispatcher):
    def __init__(self, root_path):
        super().__init__(root_path)
        self.persister_registry = {
                ".txt": TxtPersister
            }

    def execute(self, body, res):
        rel_endpoint = body.get("rel_endpoint")
        if not rel_endpoint:
            raise BadRequestException("Push request without endpoint")

        rel_path = Path(rel_endpoint)
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

        status = instance.push(content)
        return res.status(status.code, json.dumps(status.message))
