from django.conf.urls import include, url, patterns
from rest_framework import routers
from apiserver.views import UserViewSet, GroupViewSet

from django.contrib import admin
admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    # url(r'^', include('projects.urls')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
)
