from django.core.exceptions import ValidationError
from django.test import TestCase
from .validators import PHONE_REGEX


class ValidatorsTest(TestCase):
    """ Suite to test the validator functions inside validators.py

    Attributes:
    -----------
    PHONE_REGEX : RegexValidator
        This validator checks that phone numbers are properly formatted.
    """

    def test_good_phone_number(self):
        """ Test if the validator accepts a properly formatted number.

        In this case we are going to test multiple variations of properly
        formatted phone numbers. The cases are a full number, a 9 digit number
        a 15 digit number, a number with country code, and a number without a
        country code.
        """

        PHONE_REGEX('+529381124892')  # Full phone number
        PHONE_REGEX('9381124892')  # Phone number without a country code
        PHONE_REGEX('019283746510294')  # 15 digit phone number
        PHONE_REGEX('+019283746510294')  # 15 digit phone number with country code
        PHONE_REGEX('938112489')  # 9 digit phone number
        PHONE_REGEX('938112489')  # 9 digit phone number with country code

    def test_bad_phone_number(self):
        """ Test if the validator raises validation exception with bad number.

        In this case we are going to test cases where the validation should fail.
        """

        # 16 digit phone number
        self.assertRaises(ValidationError, PHONE_REGEX, '0987654321123456')
        # 16 digit phone number with country code
        self.assertRaises(ValidationError, PHONE_REGEX, '+521234567890123456')
        # Random String
        self.assertRaises(ValidationError, PHONE_REGEX, 'foo')
        # Random String with country code
        self.assertRaises(ValidationError, PHONE_REGEX, '+52foo')
