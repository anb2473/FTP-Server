from .exception import ResolutionFailedException
import json

class Resolution:
    def __init__(self, conn):
       self.conn = conn
       
    def status(self, status, message):
        header = status.to_bytes(2, byteorder='big')
        payload = json.dumps(message).encode('utf-8')

        try:
            self.conn.sendall(header + payload)
            return 0
        except Exception as e:
            raise ResolutionFailedException("An error occured while resolving request", e)
