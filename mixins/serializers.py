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
