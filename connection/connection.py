import json
from .exception import NoRequestTypeException, NoBodyException, ResolutionFailedException
from .resolution import Resolution
from .dispatcher.dispatcher_registry import pull_dispatcher

class ConnectionSession:
    def __init__(self, conn, addr, root_path):
        self.conn = conn
        self.running = True
        self.addr = addr
        self.root_path = root_path

    def package_err(self, err):
        err_name = type(err).__name__
        err_message = str(err)
        attributes = vars(err)

        return {
                "err_name": err_name,
                "err_message": err_message,
                "attributes": attributes
            }

    def run(self):
        while self.running:
            reqs = self.conn.recv(1024).decode()
            if not reqs:
                continue

            json_req = json.loads(reqs)
            try:
                self.unpack(json_req, self.dispatch)
            except ResolutionFailedException:
                raise
            except Exception as err:
                res = Resolution(self.conn)
                res.status(1, json.dumps(self.package_err(err)))
    
    def unpack(self, json_req, dispatcher):
        # Req types: GET (pull file from registry), CMP (compare file against registry), PUSH (Push new file to registry)
        req_type = json_req.get("req")
        if not req_type:
            raise NoRequestTypeException("No request type given in request (expected \"req\")", json_req)
        body = json_req.get("body")
        if not body:
            raise NoBodyException("No request body given in request (expected \"body\")", json_req)
        dispatcher(req_type, body)
        
    def dispatch(self, req_type, body):
        dispatcher = pull_dispatcher(req_type, self.root_path)
        dispatcher.execute(body, Resolution(self.conn))
