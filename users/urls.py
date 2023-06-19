from django.urls import path
from users.views import (
    AdminSignUpView, GuestSignUpView, LoginView, LogoutView, PasswordResetView, VerifyOTP, PasswordView)

urlpatterns = [
    path('admin/signup', AdminSignUpView.as_view(), name='admin_signup'),
    path('guest/signup', GuestSignUpView.as_view(), name='guest_signup'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),

    # ============================================================================
    # Reset Password
    # ============================================================================
    path("send_code", PasswordResetView.as_view(), name="send_code"),
    path("verify_otp", VerifyOTP.as_view(), name="verify_oTP"),
    path("password_confirm", PasswordView.as_view(), name="password_confirm"),
]
