class WrappedErrorResponse(Exception):
    def __init__(self, response_obj, ex, method):
        self.response_obj = response_obj
        self.exception = ex
        self.methods = [method]