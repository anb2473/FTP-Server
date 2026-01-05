import socket
from concurrent.futures import ThreadPoolExecutor
from config import *
from connection.connection import ConnectionSession
from session_manager import SessionManager
from pathlib import Path

class Server:
    def __init__(self):
        self.root_path = self.get_root()
        self.running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.sock.bind((HOST, PORT))
        self.sock.listen(MAX_CLIENT_QUEUE)
        self.pool = ThreadPoolExecutor(max_workers=MAX_THREAD_POOL)
        self.session_manager = SessionManager()
        print(f"Started remote session (Maximum Connections: {MAX_THREAD_POOL})")

    def get_root(self):
        root_path = Path(ROOT_PATH).resolve()
        root_path.mkdir(parents=True, exist_ok=True)
        return root_path

    def listen(self):
        while self.running:
            print(f"Remote listening for connections (port: {PORT})")
            conn, addr = self.sock.accept()
            print(f"Connection recieved from client (address: {addr})")
            session = ConnectionSession(conn, addr, self.root_path)
            future = self.pool.submit(session.run)
            self.session_manager.track(addr, future)

if __name__ == "__main__":
    server = Server()
    server.listen()
