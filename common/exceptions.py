from rest_framework.exceptions import APIException

class InternalUserTypeError(APIException):
    status_code = 500
    default_detail = 'Internal user type error'

class InvalidUserType(APIException):
    status_code = 400
    default_detail = 'Action unavailable for given user type'

class ExpandException(APIException):
    status_code = 400
    default_detail = 'Invalid expand parameter(s)'

class FilterException(APIException):
    status_code = 400
    default_detail = 'Invalid filter parameter(s)'
