from django.conf.urls import include, url
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

# from django.contrib import admin
# admin.autodiscover()

# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ('url', 'username', 'email', 'is_staff')
#
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)

urlpatterns = [
    # url(r'^', include(router.urls)),
    url(r'^', include('projects.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

# urlpatterns = [
#     # Examples:
#     url(r'^$', 'apiserver.views.home', name='home'),
#     # url(r'^blog/', include('blog.urls')),
#
#     url(r'^admin/', include(admin.site.urls)),
# ]
