from rest_framework.viewsets import ModelViewSet, GenericViewSet

class FilterableViewMixin(object):
    def get_serializer(self, *args, **kwargs):
        filter_params = self.request.query_params.get('filter', None)
        if filter_params: kwargs['filter'] = filter_params
        return super(FilterableViewMixin, self).get_serializer(*args, **kwargs)

class ExpandableViewMixin(object):
    def get_serializer(self, *args, **kwargs):
        expand_params = self.request.query_params.get('expand', None)
        if expand_params: kwargs['expand'] = expand_params
        return super(ExpandableViewMixin, self).get_serializer(*args, **kwargs)

class DynamicModelViewSet(FilterableViewMixin, ExpandableViewMixin, ModelViewSet):
    pass

class DynamicGenericViewSet(FilterableViewMixin, ExpandableViewMixin, GenericViewSet):
    pass
