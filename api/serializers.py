from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Pension, Schedule, Notification

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name','last_name' , 'password', 'is_superuser', 'date_joined']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()  # Use the nested serializer for user details

    class Meta:
        model = Profile
        fields = ['id', 'user', 'mobile_num', 'address']

class UserSerializer(serializers.ModelSerializer):
    mobile_num = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'password', 'mobile_num', 'is_superuser']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        mobile_num = validated_data.pop('mobile_num')
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, mobile_num=mobile_num)
        return user

class PensionSerializer(serializers.ModelSerializer):
    seniors = UserDetailSerializer()  # Use the nested serializer for user details
    class Meta:
        model = Pension
        fields = '__all__'
        
class SubmitRequirementsSerializer(serializers.ModelSerializer):
    seniors = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Accepts the User ID
    class Meta:
        model = Pension
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['id', 'description', 'month', 'startDatetime', 'endDatetime']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class PensionQrCodeSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()  # Use the nested serializer for user details
    class Meta:
        model = Pension
        fields = ['id', 'seniors', 'qr', 'status', 'notification_status']