# views.py
from rest_framework import generics, permissions, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import status
from .serializers import UserSerializer, ProfileSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Profile
from rest_framework.views import APIView
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework.decorators import api_view


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        username = validated_data.get('username')
        email = validated_data.get('email')
        mobile_num = validated_data.get('mobile_num', None)

        if User.objects.filter(username=username).exists():
            raise ValidationError({'mobile number': 'A user with this mobile number already exists.'})

        if User.objects.filter(email=email).exists():
            raise ValidationError({'email': 'A user with this email already exists.'})

        if mobile_num and Profile.objects.filter(mobile_num=mobile_num).exists():
            raise ValidationError({'mobile_num': 'A user with this mobile number already exists.'})

        # Saving the user and the profile together
        serializer.save()

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    
class ProfileView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
       
        profile = Profile.objects.get(user__id=user_id)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
        
