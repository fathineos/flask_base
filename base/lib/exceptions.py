class LibraryException(Exception):
    code = 3000
    description = "Generic Library Error"

    def __init__(self):
        Exception.__init__(self, self.code, self.description)


class NoTimezoneSet(LibraryException):
    code = 3001
    description = "No timezone set"
