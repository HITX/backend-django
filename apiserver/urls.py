from django.conf.urls import include, url, patterns
from rest_framework import routers

from apiserver.views import InternViewSet, OrgViewSet, GroupViewSet
from user_settings.views import UserSettingsView

from django.contrib import admin
admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'interns', InternViewSet)
router.register(r'orgs', OrgViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^settings/$', UserSettingsView.as_view()),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^accounts/', include(admin.site.urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
