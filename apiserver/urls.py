from django.conf.urls import include, url, patterns
from rest_framework.routers import DefaultRouter

from apiserver.routers import MeRouter
from apiserver.views import InternViewSet, OrgViewSet, GroupViewSet, MeViewSet
from user_settings.views import UserSettingsView

from django.contrib import admin
admin.autodiscover()

router = DefaultRouter()
router.register(r'interns', InternViewSet)
router.register(r'orgs', OrgViewSet)
router.register(r'groups', GroupViewSet)

meRouter = MeRouter()
meRouter.register(r'me', MeViewSet, base_name='me')

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^', include(meRouter.urls)),
    url(r'^settings/$', UserSettingsView.as_view()),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^accounts/', include(admin.site.urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
