from django.core.exceptions import ValidationError


def length_username_validator(username):
    if len(username) < 4:
        raise ValidationError('Your username is too short. It must be at least 4 characters long.')

    if len(username) > 25:
        raise ValidationError('Your username is too long. It must be 25 characters or less.')
