class ModelException(Exception):
    """Base Exception for models"""


class DoesNotExist(ModelException):
    """Exception for when instance does not exist"""
