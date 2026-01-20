
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    """
    Custom authentication backend that allows login with email address.
    Falls back to Django's default ModelBackend for other authentication methods.
    """
    
    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        # Try email first (if provided)
        if email:
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                return None
        
        # Fallback to username if email not provided
        if username:
            try:
                user = User.objects.get(username=username)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                return None
        
        return None