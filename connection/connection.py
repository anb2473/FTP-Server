import json
from .exception import NoRequestTypeException, NoBodyException, ResolutionFailedException, DispatcherNotFoundException
from .resolution import Resolution
from .dispatcher.get_dispatcher.get_dispatcher import GetDispatcher
from .dispatcher.cmp_dispatcher.cmp_dispatcher import CmpDispatcher
from .dispatcher.push_dispatcher.push_dispatcher import PushDispatcher
from .dispatcher.fetch_dispatcher.fetch_dispatcher import FetchDispatcher
from .dispatcher.delete_dispatcher.delete_dispatcher import DeleteDispatcher
from .dispatcher.dispatcher import Dispatcher

class ConnectionSession:
    def __init__(self, conn, addr, root_path):
        self.conn = conn
        self.running = True
        self.addr = addr
        self.root_path = root_path

        self.dispatcher_registry = {
            "GET": GetDispatcher,
            "CMP": CmpDispatcher,
            "PUSH": PushDispatcher,
            "FETCH": FetchDispatcher,
            "DELETE": DeleteDispatcher
        }

    def package_err(self, err):
        err_name = type(err).__name__
        err_message = str(err)
        attributes = vars(err)

        return {
                "err_name": err_name,
                "err_message": err_message,
                "attributes": str(attributes)
            }

    def run(self):
        while self.running:
            reqs = self.conn.recv(1024).decode()
            if not reqs:
                continue

            json_req = json.loads(reqs)
            # All dispatchers directly escalate errors
            # which are intercepted and safely packaged by the connection
            try:
                self.unpack(json_req, self.dispatch)
            # error in resolution is a connection error
            except ResolutionFailedException:
                raise
            except Exception as err:
                res = Resolution(self.conn)
                res.status(1, json.dumps(self.package_err(err)))

    def pull_dispatcher(self, req_type):
        dispatcher = self.dispatcher_registry.get(req_type)
        if not dispatcher:
            raise DispatcherNotFoundException("Failed to get dispatcher", req_type)
        assert issubclass(dispatcher, Dispatcher)
        instance = dispatcher(self.root_path)
        return instance
    
    def unpack(self, json_req, dispatcher):
        # Req types: 
        # -- GET (pull file from registry), 
        # -- CMP (compare file against registry), 
        # -- PUSH (Push new file to registry)
        # -- FETCH (fetch the metadata of all files)
        # -- DELETE (delete a file from the registry)

        req_type = json_req.get("req")
        if not req_type:
            raise NoRequestTypeException("No request type given in request (expected \"req\")", json_req)
        body = json_req.get("body")
        if body is None:
            raise NoBodyException("No request body given in request (expected \"body\")", json_req)

        ret_code = dispatcher(req_type, body)
        if ret_code != 0:
            raise ResolutionFailedException(f"Unknown error in resolution (ret_code: {ret_code})", None)
        
    def dispatch(self, req_type, body):
        dispatcher = self.pull_dispatcher(req_type)
        return dispatcher.execute(body, Resolution(self.conn))
