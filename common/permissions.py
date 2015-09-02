def checkAuth(request, user_type=None, scopes=None):
    user = request.user
    if not (user and user.is_authenticated()):
        return False

    if user_type and (not user.is_type(user_type)):
        return False

    if scopes:
        token = request.auth
        if not (token and token.is_valid(scopes)):
            return False

    return True


class IsAuth(object):

    @staticmethod
    def has_read_permission(request):
        return checkAuth(request, scopes=['read'])

    @staticmethod
    def has_write_permission(request):
        return checkAuth(request, scopes=['write'])

class IsAuthOrReadOnly(IsAuth):
    @staticmethod
    def has_read_permission(request):
        return True

class IsAuthOrReadOnlyAndCreate(IsAuthOrReadOnly):
    @staticmethod
    def has_create_permission(request):
        return True
