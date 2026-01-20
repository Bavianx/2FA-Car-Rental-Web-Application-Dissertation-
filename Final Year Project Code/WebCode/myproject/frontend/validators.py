from django.core.exceptions import ValidationError
import re


class ComplexPasswordValidator:
    """
    Validates password complexity requirements:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one digit
    - At least one special character
    """
    
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(
                "Password must contain at least 8 characters",
                code='password_too_short',
            )
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                "Password must contain at least one uppercase character",
                code='password_no_upper',
            )
        if not re.search(r'\d', password):
            raise ValidationError(
                "Password must contain at least one digit",
                code='password_no_digit',
            )
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(
                "Password must contain at least one special character",
                code='password_no_special',
            )
    
    def get_help_text(self):
        return (
            "Your password must contain at least 8 characters, "
            "including uppercase letters, digits, and special characters."
        )