from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from splinter import Browser


class TestAuthViews(StaticLiveServerTestCase):
    """Integration test suite for testing the views in the app: tosp_auth.

    Test all the views of this app.

    Attributes
    ----------
    username : string
        Username that will be used in the creation and testing of users.
    password : string
        Password that will be used in the creation and testing of users.
    browser : Browser
        Driver to navigate through websites and to run integration tests.
    """

    def setUp(self):
        """Initialize the browser and create a new user, before running the tests.

        """
        self.username = 'ArthurD'
        self.password = 'notAgainFord'
        get_user_model().objects.create_user(username=self.username,
                                             password=self.password)
        self.browser = Browser('chrome')

    def tearDown(self):
        """At the end of tests, close the browser

        """
        self.browser.quit()

    def test_empty_fields(self):
        """ Test for empty fields

        Visit the url of name 'login', and check that the form can't
        be submitted without filling out each field in the form. Then
        check that filling the form, allows it to be submitted.
        """
        self.browser.visit(self.live_server_url + reverse('tosp_auth:login'))
        self.browser.find_by_name('login-submit').first.click()
        self.assertTrue(self.browser.find_by_css('input:invalid'))
        self.browser.fill('username', self.username)
        self.browser.fill('password', self.password)
        self.assertFalse(self.browser.find_by_css('input:invalid'))
        self.browser.find_by_name('login-submit').first.click()
        test_string = 'Hello, world!'
        self.assertTrue(self.browser.is_text_present(test_string))

    def test_valid_login(self):
        """ Test for valid login at url 'tosp_auth:login'

        Visit the url of name 'login', fill the login form, and check
        for redirection to 'home'.

        Attributes
        ----------
        test_string : string
            This string is expected after succesful login.
        """
        self.browser.visit(self.live_server_url + reverse('tosp_auth:login'))
        self.browser.fill('username', self.username)
        self.browser.fill('password', self.password)
        self.browser.find_by_name('login-submit').first.click()
        test_string = 'Hello, world!'
        self.assertTrue(self.browser.is_text_present(test_string))

    def test_bad_password(self):
        """ Test for invalid password at url 'tosp_auth:login'

        Visit the url of name 'login', fill the login form with wrong
        password, and check for error_message.

        Attributes
        ----------
        bad_password : string
            This password is invalid for the user.
        error_message : string
            This message is expected after a failed login attempt.
        """
        bad_password = self.password + 'wrong_password'
        self.browser.visit(self.live_server_url + reverse('tosp_auth:login'))
        self.browser.fill('username', self.username)
        self.browser.fill('password', bad_password)
        self.browser.find_by_name('login-submit').first.click()
        error_message = 'El usuario o la contraseña son incorrectos.'
        self.assertTrue(self.browser.is_text_present(error_message))

    def test_bad_username(self):
        """ Test for invalid username at url 'tosp_auth:login'

        Visit the url of name 'login', fill the login form with invalid
        username, and check for error_message.

        Attributes
        ----------
        bad_username : string
            This username is invalid.
        error_message : string
            This message is expected after a failed login attempt.
        """
        bad_username = self.username + 'wrong_username'
        self.browser.visit(self.live_server_url + reverse('tosp_auth:login'))
        self.browser.fill('username', bad_username)
        self.browser.fill('password', self.password)
        self.browser.find_by_name('login-submit').first.click()
        error_message = 'El usuario o la contraseña son incorrectos.'
        self.assertTrue(self.browser.is_text_present(error_message))
