from rest_framework.exceptions import APIException

class InvalidUserType(APIException):
    status_code = 400
    default_detail = 'Action unavailable for given user type'
