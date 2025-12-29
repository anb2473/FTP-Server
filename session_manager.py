class SessionManager:
    def __init__(self):
        self.active_sessions = {}

    def track(self, addr, future):
        self.active_sessions[addr] = future
