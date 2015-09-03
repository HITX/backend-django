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



ExpandableFieldInfo = namedtuple('ExpandableFieldInfo', 'serializer kwargs')

class ExpandableFieldsMixin(object):
    def __init__(self, *args, **kwargs):
        expand_desired = kwargs.pop('expand', None)

        super(ExpandableFieldsMixin, self).__init__(*args, **kwargs)

        expand_available = getattr(self.Meta, 'expandable_fields', None)

        if not expand_available:
            if expand_desired: raise ExpandException('Expand not available for this endpoint')
            return

        self.Meta.fields += tuple(expand_available.keys())

        if expand_desired:
            desired_set = set(expand_desired.split(','))
            available_set = set(expand_available.keys())

            bad_fields = desired_set - available_set
            if bool(bad_fields):
                raise ExpandException('Expand not available for fields: ' + ','.join(bad_fields))

            for field_name in available_set - desired_set:
                expand_available.pop(field_name)

            self.fields.update({k: v.serializer(**v.kwargs) for k,v in expand_available.items()})


# Mixin order is important!
class DynamicModelSerializer(FilterableFieldsMixin, InlineFieldsMixin, ExpandableFieldsMixin, ModelSerializer):
    pass
