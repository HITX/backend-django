from rest_framework.serializers import ModelSerializer

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

class DynamicFieldsMixin(object):
    def __init__(self, *args, **kwargs):
        super(DynamicFieldsMixin, self).__init__(*args, **kwargs)
        if not self.context: return
        fields = self.context['request'].query_params.get('fields', None)
        if fields:
            fields = fields.split(',')
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class ExpandableFieldsMixin(object):
    def __init__(self, *args, **kwargs):
        expand_desired = kwargs.pop('expand', None)
        expand_available = self.Meta.expandable_fields

        super(ExpandableFieldsMixin, self).__init__(*args, **kwargs)

        if not expand_available:
            if expand_desired: raise Exception('Expand not available')
            return

        if expand_desired:
            desired_set = set(expand_desired.split(','))
            available_set = set(expand_available.keys())

            bad_fields = desired_set - available_set
            if bool(bad_fields):
                raise Exception('Expand not available for fields: ' + ','.join(bad_fields))

            undesired = []
            for field_name in set(expand_available.keys()) - set(expand_desired.split(',')):
                expand_available.pop(field_name)
                undesired.append(field_name)

            self.Meta.fields += tuple(undesired)
            self.fields.update({k: v() for k,v in expand_available.items()})
        else:
            self.Meta.fields += tuple(expand_available.keys())
            print 'No expansion desired'

class ExpandableModelSerializer(ExpandableFieldsMixin, ModelSerializer):
    pass
