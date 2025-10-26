class SbcSolverException(Exception):
    """Base exception class for SBC solver errors"""
    pass


class IncorrectFormation(SbcSolverException):
    """Exception raised when formation is incorrect"""
    pass


class IncorrectClubName(SbcSolverException):
    """Exception raised when club name is not found"""
    pass


class IncorrectNationName(SbcSolverException):
    """Exception raised when nation name is not found"""
    pass


class IncorrectLeagueName(SbcSolverException):
    """Exception raised when league name is not found"""
    pass


class IncorrectVersion(SbcSolverException):
    """Exception raised when version is not found"""
    pass


class NoSolutionFound(SbcSolverException):
    """Exception raised when no solution is found for given constraints"""
    pass