from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework.authentication import TokenAuthentication
from .models import User
from .serializers import (
    UserDataSerializer, AdminSignUpSerializer, GuestSignUpSerializer, ResetPasswordSerializer, VerifyOtpSerializer, PasswordSerializer)
from project.email_send import send_otp_via_email
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404


# ========== SignUp ================
class AdminSignUpView(generics.CreateAPIView):
    serializer_class = AdminSignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'user created successfully', }, status=status.HTTP_200_OK)


class GuestSignUpView(generics.CreateAPIView):
    serializer_class = GuestSignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'user created successfully', }, status=status.HTTP_200_OK)


# ========== Login =================
class LoginView(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            token, create = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Login Successfully",
                'data': UserDataSerializer(user).data,
                "token": token.key
            }, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Email or Password is Invalid'}, status=status.HTTP_401_UNAUTHORIZED)


# ========== Logout =================
class LogoutView(ObtainAuthToken):
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        token = request.auth
        token.delete()
        return Response({"message": "Logout Successfully"}, status=status.HTTP_200_OK)


# ============================================================================
# Reset Password
# ============================================================================
class PasswordResetView(APIView):

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            send_otp_via_email(email)
            return Response({"message": 'Code sent'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTP(APIView):

    def post(self, request):
        serializer = VerifyOtpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']

            user = get_object_or_404(User, email=email)

            if user.otp != otp:
                return Response({"message": 'Invalid code'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "Code verified"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordView(APIView):
    def post(self, request):
        data = request.data

        serializer = PasswordSerializer(data=data)
        if serializer.is_valid():
            password = serializer.data['password']
            email = serializer.data['email']
            user = get_object_or_404(User, email=email)

            user.password = make_password(password)
            user.save()

            return Response({"message": "Password Reset Successfully"}, status=status.HTTP_200_OK)
        else:
            new_error = {}
            for field_name, field_errors in serializer.errors.items():
                new_error[field_name] = field_errors[0]
            return Response(new_error, status=status.HTTP_400_BAD_REQUEST)
