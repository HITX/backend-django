from rest_framework.routers import Route, DynamicDetailRoute, SimpleRouter

class RetrieveRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={'get': 'retrieve'},
            name='{basename}-detail',
            initkwargs={'suffix': 'Instance'}
        ),
        DynamicDetailRoute(
            url=r'^{prefix}/{methodnamehyphen}{trailing_slash}$',
            name='{basename}-{methodnamehyphen}',
            initkwargs={}
        )
    ]
