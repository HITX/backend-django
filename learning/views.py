from rest_framework.viewsets import ModelViewSet
from learning.models import Learn
from learning.serializers import LearnSerializer

class LearnViewSet(ModelViewSet):
    queryset = Learn.objects.all()
    serializer_class = LearnSerializer
    permission_classes = []
