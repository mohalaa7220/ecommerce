from django.contrib.auth.backends import BaseBackend
from users.models import User
from django.shortcuts import get_object_or_404


class EmailBackend(BaseBackend):

    def authenticate(self, request, email=None, password=None, **kwargs):
        user = get_object_or_404(User, email=email)
        if user.check_password(password):
            return user
        else:
            return None
