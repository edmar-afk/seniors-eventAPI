from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['mobile_num', 'address']

class UserSerializer(serializers.ModelSerializer):
    mobile_num = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'password', 'mobile_num']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        mobile_num = validated_data.pop('mobile_num')
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, mobile_num=mobile_num)
        return user
    
        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'mobile_num', 'profile_pic']  # Ensure this matches your model fields
        

