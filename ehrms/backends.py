import email
from typing import Any
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.http.request import HttpRequest
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from ehrms.admin import UserModel

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        if user.has_usable_password():
 
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        else:
           
            if self.user_can_authenticate(user):
                return user

        return None
