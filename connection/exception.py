class ResolutionFailedException(Exception):
    def __init__(self, message, exception):
        super().__init__(message)
        self.exception = exception

class NoRequestTypeException(Exception):
    def __init__(self, message, json_req):
        super().__init__(message)
        self.req = json_req

class NoBodyException(Exception):
    def __init__(self, message, json_req):
        super().__init__(message)
        self.req = json_req

class DispatcherNotFoundException(Exception):
    def __init__(self, message, req_type):
        super().__init__(message)
        self.req_type = req_type

class PersisterNotFoundException(Exception):
    def __init__(self, message, suffix):
        super().__init__(message)
        self.suffix = suffix

class BadRequestException(Exception):
    def __init__(self, message):
        super().__init__(message)

class FileProcessorNotFoundException(Exception):
    def __init__(self, message, suffix):
        super().__init__(message)
        self.suffix = suffix

class EndpointNotFoundException(Exception):
    def __init__(self, message, endpoint):
        super().__init__(message)
        self.rel_endpoint = endpoint

class ResourceIsDirectoryException(Exception):
    def __init__(self, message, absolute_path):
        super().__init__(message)
        self.absolute_path = absolute_path

class MetaNotFoundException(Exception):
    def __init__(self, message, meta_path):
        super().__init__(message)
        self.meta_path = meta_path

class ResourceIsFileException(Exception):
    def __init__(self, message, absolute_path):
        super().__init__(message)
        self.absolute_path = absolute_path
