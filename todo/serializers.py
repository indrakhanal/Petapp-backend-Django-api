from statistics import mode
from rest_framework import serializers
from .models import Todo
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class TodoSerializers(serializers.ModelSerializer):
    class Meta:
        model=Todo
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token