from get_dispatcher.get_dispatcher import GetDispatcher
from cmp_dispatcher.cmp_dispatcher import CmpDispatcher
from push_dispatcher.push_dispatcher import PushDispatcher
from dispatcher import Dispatcher

class InvalidDispatcherException(Exception):
    def __init__(self, message, dispatcher):
        super().__init__(message)
        self.dispatcher = dispatcher

class InvalidRequestTypeException(Exception):
    def __init__(self, message, req_type):
        super().__init__(message)
        self.req_type = req_type

dispatcher_registry = {
        "GET": GetDispatcher,
        "CMP": CmpDispatcher,
        "PUSH": PushDispatcher
    }

def pull_dispatcher(req_type):
    dispatcher = dispatcher_registry.get(req_type).__init__()
    if not dispatcher:
        raise InvalidRequestTypeException("Request contains an invalid request type, no dispatcher available", req_type)
    if not isinstance(dispatcher, Dispatcher):
       raise InvalidDispatcherException("Dispatcher registry returned non dispatcher", dispatcher)
    return dispatcher
