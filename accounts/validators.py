from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomMinimumLengthValidator:
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _("This password is too short. It must contain at least %(min_length)d characters."),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return _("Your password must contain at least %(min_length)d characters.") % {'min_length': self.min_length}

class CustomUserAttributeSimilarityValidator:
    def validate(self, password, user=None):
        if user and user.username and user.username in password:
            raise ValidationError(
                _("The password is too similar to the username."),
                code='password_too_similar',
            )

    def get_help_text(self):
        return _("Your password cannot be too similar to your username.")
