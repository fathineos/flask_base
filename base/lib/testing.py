import unittest
from pkgutil import walk_packages

"""TestCase class provides provide unit testing functionality. On setUp a new
flask app is instantiated with testing configuration and a new application
context is started
"""


class TestCase(unittest.TestCase):
    def setUp(self, app=None, prerequired_packages=[]):
        if not app:
            from os.path import abspath, dirname, split
            from base.app import create
            basepath = split(abspath(dirname(__file__)))[0]
            app = create(forced_environment="testing", basepath=basepath)
        self.app = app
        self.app.testing = True
        self._import_submodules(prerequired_packages)
        self.app.DB.create_all()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app.DB.drop_all()
        self.app_context.pop()

    def _import_submodules(self, prerequired_packages):
        for package in prerequired_packages:
            prefix = package.__name__ + "."
            for importer, modname, ispkg in walk_packages(package.__path__,
                                                          prefix):
                __import__(modname)


class ControllerTestCase(TestCase):
    def setUp(self, app=None):
        super(ControllerTestCase, self).setUp(app=app)
        self.app_request_context = self.app.test_request_context(
            content_type="application/json")
        self.app_request_context.push()

    def tearDown(self):
        self.app_request_context.pop()
        super(ControllerTestCase, self).tearDown()
