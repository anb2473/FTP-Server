from .get_dispatcher.get_dispatcher import GetDispatcher
from .cmp_dispatcher.cmp_dispatcher import CmpDispatcher
from .push_dispatcher.push_dispatcher import PushDispatcher

dispatcher_registry = {
    "GET": GetDispatcher,
    "PUSH": PushDispatcher,
    "CMP": CmpDispatcher
}

def pull_dispatcher(req_type):
    return dispatcher_registry[req_type]
