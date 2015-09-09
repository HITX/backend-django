from oauth2_provider.ext.rest_framework import TokenHasScope, TokenHasReadWriteScope

class DebugTokenHasScope(TokenHasScope):
    def has_permission(self, request, view):
        # If token not set (due to session authentication) allow access
        if not request.auth:
            return True

        # Otherwise behave as per normal
        super(DebugTokenHasScope, self).has_permission(request, view)



class DebugTokenHasReadWriteScope(TokenHasReadWriteScope):
    def has_permission(self, request, view):
        # If token not set (due to session authentication) allow access
        if not request.auth:
            return True

        # Otherwise behave as per normal
        super(DebugTokenHasReadWriteScope, self).has_permission(request, view)
