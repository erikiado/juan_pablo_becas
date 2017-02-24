from django.core.validators import RegexValidator

PHONE_REGEX_MESSAGE = 'Phone number must be entered in the format: "+999999999" '\
                      'Up to 15 numbers allowed'

PHONE_REGEX = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=PHONE_REGEX_MESSAGE)
