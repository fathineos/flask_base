"""Exception classes to extend BasicException functionality. The basic
types provided are MutableException and ImmutableException. Both shall
have the same interface."""


class IException(object):
    """Interface for Custom Exception classes.
    functions to be implemented: get_code, get_description
    """
    def get_code(self):
        raise Exception("Exception 3002: Not Implemented")

    def get_description(self):
        raise Exception("Exception 3002: Not Implemented")


class MutableException(IException, Exception):
    """
    This exception class extends python's basic exception and allows you to set
    custom code and description
    :param code: an exception code
    :param message: a description of the exception
    :type code: int
    :type message: str
    """
    def __init__(self, code, description):
        self.__code = code
        self.__description = description
        message = "Exception {}: {}".format(self.__code, self.__description)
        Exception.__init__(self, message)

    def get_code(self):
        return self.__code

    def get_description(self):
        return self.__description


class ImmutableException(IException, Exception):
    """
    This exception class extends python's basic exception. The code, and
    description is immutable. Extend this class to create more specific
    exceptions.
    """
    _code = 1000
    _description = "Generic Error"

    def __init__(self):
        message = "Exception {}: {}".format(self._code, self._description)
        Exception.__init__(self, message)

    def get_code(self):
        return self._code

    def get_description(self):
        return self._description


class LibraryException(ImmutableException):
    _code = 3000
    _description = "Generic Library Error"


class NoTimezoneSet(LibraryException):
    _code = 3001
    _description = "No timezone set"


class InterfaceException(ImmutableException):
    _code = 3002
    _description = "Not Implemented"
