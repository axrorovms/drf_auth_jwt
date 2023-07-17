from django.urls import path
from auth_system.views import (
    UserTokenObtainPairView, UserTokenRefreshView, UserTokenVerifyView,
    RegisterUserCreateAPIView, ActivationUserGenericAPIView, PasswordResetGenericAPIView, PasswordResetConfirmUpdateAPIView
)
app_name = 'auth_system'
urlpatterns = [
    path('token/create/', UserTokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', UserTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', UserTokenVerifyView.as_view(), name='token_verify'),
    path('register/', RegisterUserCreateAPIView.as_view(), name='register'),
    path('activated-account/', ActivationUserGenericAPIView.as_view(), name='activated_account'),
    path('reset-password/', PasswordResetGenericAPIView.as_view(), name='reset_password'),
    path('reset-password-confirm/', PasswordResetConfirmUpdateAPIView.as_view(), name='reset_password_confirm'),
]
