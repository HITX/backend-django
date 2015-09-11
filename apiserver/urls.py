from django.conf.urls import include, url, patterns
from rest_framework.routers import DefaultRouter

from common.routers import RetrieveOnlyRouter
from apiserver.views import InternViewSet, OrgViewSet, GroupViewSet
from me.views import MeViewSet
# from user_settings.views import UserSettingsView
from projects.views import ProjectViewSet
from submissions.views import SubmissionViewSet

from newsfeed.views import NewsfeedViewSet

from django.contrib import admin
admin.autodiscover()

router = DefaultRouter()
router.register(r'interns', InternViewSet)
router.register(r'orgs', OrgViewSet)
router.register(r'groups', GroupViewSet)

router.register(r'projects', ProjectViewSet)
router.register(r'submissions', SubmissionViewSet)

retrieveOnlyRouter = RetrieveOnlyRouter()
retrieveOnlyRouter.register(r'me', MeViewSet, base_name='me')
retrieveOnlyRouter.register(r'newsfeed', NewsfeedViewSet)


urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^', include(retrieveOnlyRouter.urls)),
    # url(r'^settings/$', UserSettingsView.as_view()),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    # url(r'^accounts/', include(admin.site.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
