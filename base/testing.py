import unittest
from base.app import create

"""TestCase class provides provide unit testing functionality. On setUp a new
flask app is instanciated with testing configuration and a new application
context is started
"""


class TestCase(unittest.TestCase):
    def setUp(self):
        self.app = create(forced_environment="testing")
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()
