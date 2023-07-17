from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework.generics import CreateAPIView, GenericAPIView

from auth_system.models import User
from auth_system.serializers import RegisterUserModelSerializer, CheckActivationSerializer, SendEmailResetSerializer
from auth_system.serializers.serializers import PasswordResetConfirmSerializer


# Create your views here.

class UserTokenObtainPairView(TokenObtainPairView):
    parser_classes = (FormParser, MultiPartParser)


class UserTokenRefreshView(TokenRefreshView):
    parser_classes = (FormParser, MultiPartParser)


class UserTokenVerifyView(TokenVerifyView):
    parser_classes = (FormParser, MultiPartParser)


class RegisterUserCreateAPIView(CreateAPIView):
    serializer_class = RegisterUserModelSerializer
    parser_classes = (FormParser, MultiPartParser)


class ActivationUserGenericAPIView(GenericAPIView):
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = CheckActivationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=serializer.validated_data.get('email'))
        user.is_active = True
        user.save(update_fields=["is_active"])
        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordResetGenericAPIView(GenericAPIView):
    serializer_class = SendEmailResetSerializer
    parser_classes = (FormParser, MultiPartParser)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        return Response({'email': email}, status=status.HTTP_200_OK)


class PasswordResetConfirmUpdateAPIView(GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    parser_classes = (FormParser, MultiPartParser)

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get('new_password')
        user = User.objects.get(email=serializer.validated_data.get('email'))
        user.password = make_password(password)
        user.save(update_fields=["password"])
        return Response(status=status.HTTP_200_OK)
