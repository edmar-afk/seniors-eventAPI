# views.py
from rest_framework import generics, permissions, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import status
from .serializers import UserSerializer, ProfileSerializer, ScheduleSerializer, PensionSerializer, PensionQrCodeSerializer, SubmitRequirementsSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Profile, Schedule, Pension
from rest_framework.views import APIView
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework.decorators import api_view
from .utils import generate_qr_code  # Import the function here
from django.core.files.base import ContentFile
from io import BytesIO
import qrcode

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

class SeniorsListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]  # Allows unrestricted access

class SeniorView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

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
        

class ScheduleCreateView(generics.CreateAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        print("Request Data:", request.data)  # Print request data to see what is being sent
        response = super().post(request, *args, **kwargs)
        print("Response Data:", response.data)  # Print response data to see the result
        return response
    
class ScheduleListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        schedules = Schedule.objects.all()
        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data)
    

class PensionCreateView(generics.CreateAPIView):
    serializer_class = SubmitRequirementsSerializer
    permission_classes = [AllowAny]
    
    def get(self, request, senior_id):
        return Response({'detail': 'Use POST to submit a pension file.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, senior_id):
        try:
            senior = User.objects.get(id=senior_id)
        except User.DoesNotExist:
            return Response({'error': 'Senior not found'}, status=status.HTTP_404_NOT_FOUND)

        # Prepare data for the serializer
        data = request.data.copy()
        data['seniors'] = senior.id  # Use the senior's ID directly
        if 'notification_status' not in data:
            data['notification_status'] = 'Notification not Sent'

        # Debug: Print data to check the format
        print("Request Data:", data)

        # Use the serializer with the modified data
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Serializer Errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class PensionListView(generics.ListAPIView):
    serializer_class = PensionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Pension.objects.filter(seniors__id=user_id)


class DeletePensionView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, pension_id, *args, **kwargs):
        # Fetch the pension object by ID
        pension = get_object_or_404(Pension, id=pension_id)

        # Delete the pension object
        pension.delete()

        return Response({"message": "Pension deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    

class AllPensionListView(generics.ListAPIView):
    queryset = Pension.objects.all()
    serializer_class = PensionSerializer
    permission_classes = [AllowAny]
  
  
  
class AddQrCodeToPension(generics.CreateAPIView):
    serializer_class = PensionSerializer
    permission_classes = [AllowAny]

    def post(self, request, pension_id):
        # Get the pension object by ID
        pension = get_object_or_404(Pension, id=pension_id)

        # Generate QR code content
        qr_content = f"Pension ID: {pension.id}\nUser: {pension.seniors.username}\nStatus: {pension.status}"

        # Generate QR code
        qr_image = qrcode.make(qr_content)
        qr_io = BytesIO()
        qr_image.save(qr_io, format="PNG")
        qr_file = ContentFile(qr_io.getvalue(), f"{pension.id}_qr.png")

        # Save QR code to the pension object
        pension.qr.save(f"{pension.id}_qr.png", qr_file)
        pension.save()

        # Serialize the response
        response_data = {
            "pension_id": pension.id,
            "username": pension.seniors.username,
            "status": pension.status,
            "qr_code_url": pension.qr.url  # Assuming the QR code is stored as an image file
        }

        return Response(response_data, status=status.HTTP_200_OK)