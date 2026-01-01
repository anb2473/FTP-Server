import hmac
import json
from ..dispatcher import Dispatcher
from pathlib import Path
from ..hasher.txt_hasher import TxtHasher
from ..hasher.hasher import Hasher
from ...exception import FileProcessorNotFoundException, BadRequestException, MetaNotFoundException, EndpointNotFoundException
from ...status import StatusDivergent, StatusUnrelated, StatusSynced, StatusRemoteAhead, StatusLocalAhead

class CmpDispatcher(Dispatcher):
    def __init__(self, root_path):
        super().__init__(root_path)
        self.hasher_registry = {
                ".txt": TxtHasher
            }

    def check_hash(self, body, absolute_path):
        suffix = absolute_path.suffix
        hasher = self.hasher_registry.get(suffix)
        if not hasher:
            raise FileProcessorNotFoundException("Failed to load hasher - unsupported filetype", suffix)
      
        assert issubclass(hasher, Hasher)
        instance = hasher(absolute_path)

        stored_hash = instance.hash()
        recieved_hash = body.get("hash")
        if not recieved_hash:
            raise BadRequestException("Compare request without hash")
        
        return hmac.compare_digest(stored_hash, recieved_hash)
   
    def find_latest_sync(self, stored_metadata, recieved_metadata):
        recieved_metadata_set = {val: idx for idx, val in enumerate(recieved_metadata)}
        for i in range(len(stored_metadata) - 1, -1, -1):
            if stored_metadata[i] in recieved_metadata_set:
                return i, recieved_metadata_set[stored_metadata[i]]

        # Completely divergent histories
        return None, None

    def cmp_meta(self, body, absolute_path):
        meta_path = absolute_path.with_suffix(absolute_path.suffix + ".meta")
        if not meta_path.exists():
            raise MetaNotFoundException("No meta data for requested file", meta_path)

        with open(meta_path, "r") as f:
            stored_metadata = json.load(f)
        
        recieved_metadata = body.get("metadata")
        if not recieved_metadata:
            raise BadRequestException("Compare request without metadata")

        latest_sync_in_stored, latest_sync_in_recieved = self.find_latest_sync(stored_metadata, recieved_metadata)
        stored_metadata_len = len(stored_metadata) - 1
        recieved_metadata_len = len(recieved_metadata) - 1

        if latest_sync_in_stored is None or latest_sync_in_recieved is None:
            return StatusUnrelated()
        if latest_sync_in_stored == stored_metadata_len and latest_sync_in_recieved == recieved_metadata_len:
            return StatusSynced()
        if latest_sync_in_stored < stored_metadata_len and latest_sync_in_recieved < recieved_metadata_len:
            return StatusDivergent()
        if latest_sync_in_stored == stored_metadata_len and latest_sync_in_recieved < recieved_metadata_len:
            return StatusRemoteAhead()
        if latest_sync_in_stored < stored_metadata_len  and latest_sync_in_recieved == recieved_metadata_len:
            return StatusLocalAhead()

        raise RuntimeError("Unexpected state in metadata comparison")

    def execute(self, body, res):
        rel_endpoint = body.get("rel_endpoint")        
        if not rel_endpoint:
            raise BadRequestException("Hash request without endpoint")
        
        absolute_path = self.root_path / Path(rel_endpoint)
        if not absolute_path.exists():
            raise EndpointNotFoundException("Failed to fetch endpoint in root", absolute_path)

        same_hash = self.check_hash(body, absolute_path)

        status = StatusSynced()
        if not same_hash:
            status = self.cmp_meta(body, absolute_path)
        return res.status(status.code, json.dumps(status.message))
