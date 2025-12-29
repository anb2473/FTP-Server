class Resolution:
    def __init__(self, conn):
       self.conn = conn
       
    def status(self, status, message):
        header = status.to_bytes(2, byteorder='big')
        payload = message.encode('utf-8')

        self.conn.sendall(header + payload)
