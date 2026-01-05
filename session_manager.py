import traceback
from functools import partial

class SessionManager:
    def __init__(self):
        self.active_sessions = {}

    def check_for_errors(self, addr, future):
        try:
            # future.result will throw an error if the thread failed
            future.result()
        except Exception:
            print(f"Error occured in connection with client (address: {addr})")
            traceback.print_exc()

    def track(self, addr, future):
        self.active_sessions[addr] = future
        callback = partial(self.check_for_errors, addr)
        future.add_done_callback(callback)
