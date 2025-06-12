from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

class AuthorSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        extra_kwargs = {
            'email': {
                'write_only': True
            },
            'password': {
                'write_only': True
            }
        }
        fields = [
            'id', 'username', 'first_name',
            'last_name', 'email', 'password'
        ]