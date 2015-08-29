def _checkAuth(request, auth_user_type):
    user = request.user
    token = request.auth

    if (user and token and
        user.is_authenticated() and
        token.is_valid(['read'])):

        if (auth_user_type):
            print 'Auth user type was set and checked!'

        if (auth_user_type and
            user.is_type(auth_user_type)):
            return True

    return False


class IsAuthenticated():

    @staticmethod
    def has_read_permission(request, auth_user_type=None):
        return _checkAuth(request, auth_user_type)

    @staticmethod
    def has_write_permission(request, auth_user_type=None):
        return _checkAuth(request, auth_user_type)

class IsAuthenticatedOrReadOnly(IsAuthenticated):
    @staticmethod
    def has_read_permission(request):
        return True

class IsAuthenticatedOrReadOnlyAndCreate(IsAuthenticatedOrReadOnly):
    @staticmethod
    def has_create_permission(request):
        return True
