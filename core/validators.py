from django.core.validators import RegexValidator

PHONE_REGEX_MESSAGE = 'El número de telefono tiene que tener el siguiente formato: "+999999999" '\
                      'El número tiene que tener entre 9 y 15 dígitos.'

PHONE_REGEX = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=PHONE_REGEX_MESSAGE)
