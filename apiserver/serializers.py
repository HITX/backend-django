from django.contrib.auth.models import Group

from django.core.validators import RegexValidator

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apiserver.models import User
from apiserver.validators import RequiredValidator
from profiles.serializers import ProfileSerializer

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'email',
            'profile',
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }
        error_messages = {
            'username': {
                'names': {
                    'required': 'Test username required message'
                },
                'validators': {
                    UniqueValidator: 'A user with that username already exists',
                    RegexValidator: 'Invalid username'
                }
            }
        }
        # validators = [
        #     RequiredValidator(fields=('username', 'email', 'password'))
        # ]

    def create(self, validated_data):
        return User.objects.create(validated_data)

    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)

        # print self.fields['username'].error_messages
        # print self.fields['username'].validators
        # self.fields['email'].error_messages['required'] = 'test required message'
        # self.fields['username'].validators[1].message = 'test unique message'

        # name_messages = self.Meta.error_messages.names
        # validator_messages = self.Meta.error_messages.validators
        #
        # print name_messages
        # print validator_messages

        messages = self.Meta.error_messages
        # print messages

        for field_name in messages:

            # print field_name + ':'

            # print messages[field_name]
            # print messages[field_name]['names']

            # Handle names
            for name, message in messages[field_name]['names'].items():
                # print name + ' - ' + message
                self.fields[field_name].error_messages[name] = message

            # Handle validators
            validator_keys = messages[field_name]['validators']
            for validator in self.fields[field_name].validators:
                if type(validator) in validator_keys:
                    validator.message = validator_keys[type(validator)]

        # for field_name, validator_keys in messages.items():
        #     print field_name
        #     print self.fields[field_name].error_messages
        #
        #     for validator in self.fields[field_name].validators:
        #         if type(validator) in validator_keys:
        #             validator.message = validator_keys[type(validator)]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
