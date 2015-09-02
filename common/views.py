from rest_framework.viewsets import ModelViewSet

class ExpandableViewMixin(object):
    def get_serializer(self, *args, **kwargs):
        expand_params = self.request.query_params.get('expand', None)
        if expand_params:
            kwargs['expand'] = expand_params
        return super(ExpandableViewMixin, self).get_serializer(*args, **kwargs)

class ExpandableModelViewSet(ExpandableViewMixin, ModelViewSet):
    pass
