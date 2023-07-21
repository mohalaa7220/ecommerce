from django.urls import path
from users.views import (
    AdminSignUpView, GuestSignUpView, LoginView, ProfileView, LogoutView, SendCodeView, VerifyOTP, PasswordView)

urlpatterns = [
    path('signup_admin', AdminSignUpView.as_view(), name='admin_signup'),
    path('signup_user', GuestSignUpView.as_view(), name='guest_signup'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),

    path('profile', ProfileView.as_view(), name='profile'),

    # ============================================================================
    # Reset Password
    # ============================================================================
    path("send_code", SendCodeView.as_view(), name="send_code"),
    path("verify_otp", VerifyOTP.as_view(), name="verify_oTP"),
    path("password_confirm", PasswordView.as_view(), name="password_confirm"),
]
