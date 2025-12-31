import socket
from concurrent.futures import ThreadPoolExecutor
from config import *
from connection.connection import ConnectionSession
from session_manager import SessionManager
from pathlib import Path

def validate_root():
    root_path = Path(ROOT_PATH).resolve()
    root_path.mkdir(parents=True, exist_ok=True)
    return root_path

class Server:
    def __init__(self, root_path):
        self.root_path = root_path
        self.running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.sock.bind((HOST, PORT))
        self.sock.listen(MAX_CLIENT_QUEUE)
        self.pool = ThreadPoolExecutor(max_workers=MAX_THREAD_POOL)
        self.session_manager = SessionManager()
        print(f"Starting server on port {PORT}")

    def listen(self):
        while self.running:
            print("Listening for connections")
            conn, addr = self.sock.accept()
            print(f"Connection from {addr}")
            session = ConnectionSession(conn, addr, self.root_path)
            future = self.pool.submit(session.run)
            self.session_manager.track(addr, future)

if __name__ == "__main__":
    root_path = validate_root()
    server = Server(root_path)
    server.listen()
