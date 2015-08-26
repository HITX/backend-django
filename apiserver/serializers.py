from django.contrib.auth.models import Group

from django.core.validators import RegexValidator

from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator

from apiserver.models import User
from apiserver.validators import RequiredValidator
from profiles.serializers import ProfileSerializer

from mixins.serializers import ErrorMessages

class UserSerializer(ErrorMessages, ModelSerializer):
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
                'names': { 'required': 'Username is required' },
                'validators': {
                    UniqueValidator: 'A user with that username already exists',
                    RegexValidator: 'Invalid username'
                }
            },
            'email': {
                'names': { 'required': 'Email is required' },
                'validators': { UniqueValidator: 'A user with that email already exists' }
            },
            'password': {
                'names': { 'required': 'Password is required' }
            }
        }

    def create(self, validated_data):
        return User.objects.create(validated_data)


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
