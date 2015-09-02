from rest_framework.exceptions import APIException

class InvalidUserType(APIException):
    status_code = 400
    default_detail = 'Action unavailable for given user type'

class ExpandException(APIException):
    status_code = 400
    default_detail = 'Invalid expand parameter(s)'

class FilterException(APIException):
    status_code = 400
    default_detail = 'Invalid filter parameter(s)'
