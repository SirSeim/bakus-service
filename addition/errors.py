from rest_framework import status
from rest_framework.exceptions import APIException


class ModelException(Exception):
    """Base Exception for models"""


class DoesNotExist(ModelException):
    """Exception for when instance does not exist"""


class InvalidCompleteAddition(APIException):
    """Addition asked for is not marked Completed, meaning still downloading"""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Addition asked for is not marked Completed"
