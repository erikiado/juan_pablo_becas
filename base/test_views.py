from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from splinter import Browser

test_url = 'http://localhost:8081/'

class TestBaseViews(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = Browser('chrome')

    def tearDown(self):
        self.browser.quit()

    def test_home(self):
        self.browser.visit(test_url)
        test_string = 'Hello, world!'
        if self.browser.is_text_present(test_string):
            self.assertTrue(True)

    def test_robots(self):
        self.browser.visit(test_url + 'robots.txt')
        if self.browser.is_text_present('robotstxt'):
            self.assertTrue(True)

    def test_humans(self):
        self.browser.visit(test_url + 'humans.txt')
        if self.browser.is_text_present('humanstxt'):
            self.assertTrue(True)
