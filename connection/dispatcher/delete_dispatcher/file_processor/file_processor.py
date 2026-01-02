from connection.status import StatusDeleteFailed


class FileProcessor:
    def __init__(self, path):
        self.path = path

    def process(self):
        return StatusDeleteFailed()
