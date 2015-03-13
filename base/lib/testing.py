import unittest

"""TestCase class provides provide unit testing functionality. On setUp a new
flask app is instantiated with testing configuration and a new application
context is started
"""


class TestCase(unittest.TestCase):
    def setUp(self, app=None):
        if not app:
            from os.path import abspath, dirname, split
            from base.app import create
            basepath = split(abspath(dirname(__file__)))[0]
            app = create(forced_environment="testing", basepath=basepath)
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()
