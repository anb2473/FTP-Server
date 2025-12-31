from .get_dispatcher.get_dispatcher import GetDispatcher
from .cmp_dispatcher.cmp_dispatcher import CmpDispatcher
from .push_dispatcher.push_dispatcher import PushDispatcher
from .dispatcher import Dispatcher

class DispatcherNotFoundException(Exception):
    def __init__(self, message, req_type):
        super().__init__(message)
        self.req_type = req_type

dispatcher_registry = {
        "GET": GetDispatcher,
        "CMP": CmpDispatcher,
        "PUSH": PushDispatcher
    }

def pull_dispatcher(req_type, root_path):
    dispatcher = dispatcher_registry.get(req_type)
    if not dispatcher:
        raise DispatcherNotFoundException("Failed to get dispatcher", req_type)
    assert issubclass(dispatcher, Dispatcher)
    instance = dispatcher(root_path)
    return instance
