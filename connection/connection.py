import json
from .resolution import Resolution
from .dispatcher.dispatcher import Dispatcher
from .dispatcher.dispatch_registry import pull_dispatcher

class NoRequestTypeException(Exception):
    def __init__(self, message, json_req):
        super().__init__(message)
        self.req = json_req



class ConnectionSession:
    def __init__(self, conn, addr, root_path):
        self.conn = conn
        self.running = True
        self.addr = addr
        self.root_path = root_path

    def run(self):
        while self.running:
            reqs = self.conn.recv(1024).decode()
            if not reqs:
                continue

            json_req = json.loads(reqs)
            self.unpack(json_req, self.dispatch)
    
    def unpack(self, json_req, dispatcher):
        # Req types: GET (pull file from registry), CMP (compare file against registry), PUSH (Push new file to registry)
        req_type = json_req.get("req")
        if not req_type:
            raise NoRequestTypeException("No request type given in request JSON", json_req)
        body = json_req.get("body")
        dispatcher(req_type, body)
        
    def dispatch(self, req_type, body):
        dispatcher = pull_dispatcher(req_type)
        dispatcher.execute(body, self.root_path, Resolution(self.conn))
