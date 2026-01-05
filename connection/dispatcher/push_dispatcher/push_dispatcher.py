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

    def persist_content(self, absolute_path, content, rel_endpoint):
        suffix = absolute_path.suffix
        persister = self.persister_registry.get(suffix)
        if not persister:
            raise PersisterNotFoundException("Persister not found in registry - unsupported filetype", suffix)

        assert issubclass(persister, Persister)
        instance = persister(absolute_path, rel_endpoint, self.root_path)

        status = instance.push(content)
        return status

    def execute(self, body, res):
        rel_endpoint = body.get("rel_endpoint")
        if not rel_endpoint:
            raise BadRequestException("Push request without endpoint")

        content = body.get("content")
        if not content:
            raise BadRequestException("Push request without content")

        absolute_path = self.root_path / Path(rel_endpoint.lstrip("/"))

        status = self.persist_content(absolute_path, content, rel_endpoint)
        
        return res.status(status.code, status.message)
