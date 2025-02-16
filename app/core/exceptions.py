class SpaceXAPIException(Exception):
    """Raised when there's an error with the SpaceX API."""
    pass 

class CacheException(Exception):
    """Raised when there's an error with the caching system."""
    pass 

class ValidationException(Exception):
    """Raised when there's a validation error"""
    pass 