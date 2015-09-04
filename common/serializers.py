from collections import namedtuple

from rest_framework.serializers import ModelSerializer

from common.exceptions import ExpandException, FilterException

class ErrorMessagesMixin(object):
    def __init__(self, *args, **kwargs):
        messages = self.Meta.error_messages
        for field_name in messages:
            names = messages[field_name].get('names', None)
            validator_keys = messages[field_name].get('validators', None)

            # Handle names
            if names:
                for name, message in names.items():
                    self.fields[field_name].error_messages[name] = message

            # Handle validators
            if validator_keys:
                for validator in self.fields[field_name].validators:
                    if type(validator) in validator_keys:
                        validator.message = validator_keys[type(validator)]

        super(ErrorMessagesMixin, self).__init__(*args, **kwargs)


class InlineFieldsMixin(object):
    def __init__(self, *args, **kwargs):
        super(InlineFieldsMixin, self).__init__(*args, **kwargs)

        inline_fields = getattr(self.Meta, 'inline_fields', None)
        if inline_fields:
            for field_name in set(inline_fields.keys()):
                related_fields = inline_fields[field_name]().fields
                for related_field_name in related_fields:
                    new_field = related_fields[related_field_name]
                    new_field.source = field_name + '.' + new_field.source
                    self.fields[related_field_name] = new_field


class FilterableFieldsMixin(object):
    def __init__(self, *args, **kwargs):
        filter_desired = kwargs.pop('filter', None)

        super(FilterableFieldsMixin, self).__init__(*args, **kwargs)

        if filter_desired:
            desired = set(filter_desired.split(','))
            available = set(self.fields.keys())

            bad_fields = desired - available
            if bool(bad_fields):
                raise FilterException('Filter not available for fields: ' + ','.join(bad_fields))

            for field_name in available - desired:
                self.fields.pop(field_name)


class ExpandableInfo(object):
    def __init__(self, serializer, **kwargs):
        self.serializer = serializer
        self.serializer_kwargs = kwargs

    def get_serializer_instance(self, **kwargs):
        tmp = self.serializer_kwargs.copy()
        tmp.update(kwargs)
        return self.serializer(**tmp)

def _deserialize_expand_helper(prev, cur):
    if '.' in cur:
        tmp = cur.split('.', 1)
        if tmp[0] in prev:
            prev[tmp[0]] += (',' + tmp[1])
        else:
            prev[tmp[0]] = tmp[1]
    else:
        prev[cur] = None
    return prev

def _deserialize_expand_params(params_string):
    return reduce(_deserialize_expand_helper, params_string.split(','), {})

class ExpandableFieldsMixin(object):
    def __init__(self, *args, **kwargs):
        expand_desired = kwargs.pop('expand', None)

        super(ExpandableFieldsMixin, self).__init__(*args, **kwargs)

        expand_available = getattr(self.Meta, 'expandable_fields', None)

        if not expand_available:
            if expand_desired: raise ExpandException('Expand not available')
            return

        self.Meta.fields += tuple(expand_available.keys())

        if expand_desired:
            expand_desired = _deserialize_expand_params(expand_desired)

            desired_set = set(expand_desired.keys())
            available_set = set(expand_available.keys())

            bad_fields = desired_set - available_set
            if bool(bad_fields):
                raise ExpandException('Expand not available for fields: ' + ','.join(bad_fields))

            for field_name in desired_set:
                self.fields[field_name] = (
                    expand_available[field_name]
                    .get_serializer_instance(expand=expand_desired[field_name])
                )


# Mixin order is important!
class DynamicModelSerializer(FilterableFieldsMixin, InlineFieldsMixin, ExpandableFieldsMixin, ModelSerializer):
    pass
