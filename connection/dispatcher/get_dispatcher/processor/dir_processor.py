from connection.exception import EndpointNotFoundException, ResourceIsFileException


class DirProcessor:
    def __init__(self, path):
        self.path = path

    def process(self):
        if not self.path.exists():
            raise EndpointNotFoundException("Cannot GET nonexistent endpoint", self.path)

        if self.path.is_file():
            raise ResourceIsFileException("Cannot GET file as directory", self.path)

        contents = self.path.iterdir()
        return list(contents)
