from rest_framework.serializers import ModelSerializer
from .models import *
from rest_framework import serializers

# 手机号注册
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id','mobile', 'email', 'account', 'avatar', 'username', 'last_login')