from sys import prefix, modules
from os import environ
from os.path import abspath, dirname, split
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from logging import FileHandler
from base.lib.testing import TestCase
from base.factory import create_app, _get_environment, _init_sql_db,\
    _get_basepath, _register_app_loggers,\
    ENVIRONMENT_DEVELOPMENT, ENVIRONMENT_TESTING
from base.app.controllers.blueprints import blueprints


BASEPATH = split(split(abspath(dirname(__file__)))[0])[0]


class TestFactory(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_app_return_proper_instance(self):
        flask_app = create_app(package_name="base.app")
        self.assertIsInstance(flask_app, Flask)

    def test_get_application_env_when_override_variable_is_set(self):

        flask_app = create_app(package_name="base.app")
        result_env = _get_environment(app=flask_app,
                                      forced_environment=ENVIRONMENT_TESTING,
                                      basepath=BASEPATH)
        self.assertEqual(ENVIRONMENT_TESTING, result_env)

    def test_get_application_env_when_os_environment_variable_is_not_set(self):
        flask_app = create_app(package_name="base.app")
        self.assertEqual(ENVIRONMENT_DEVELOPMENT,
                         _get_environment(app=flask_app,
                                          forced_environment=None,
                                          basepath=BASEPATH))

    def test_get_application_env_when_os_environment_variable_is_set(self):
        flask_app = create_app(package_name="base.app")
        environ["APPLICATION_ENV"] = ENVIRONMENT_TESTING
        self.assertEqual(ENVIRONMENT_TESTING,
                         _get_environment(app=flask_app,
                                          forced_environment=None,
                                          basepath=BASEPATH))

    def test_app_configs_registered_proper_configuration_packages(self):
        create_app(package_name="base.app",
                   forced_environment=ENVIRONMENT_TESTING)
        self.assertIn("base.app.configs.default", modules)
        self.assertIn("base.app.configs.testing", modules)

    def test_get_sql_db_load_sqlalchemy_package_when_configured_accordingly(
            self):
        test_flask_app = Flask(
            "base.test_app",
            instance_path=(prefix + '/config/'),
            instance_relative_config=True,
            static_folder='public')

        test_flask_app.config["PACKAGE_SQLALCHEMY_ENABLED"] = True
        _init_sql_db(test_flask_app)
        self.assertIn("sqlalchemy", modules)
        from base.factory import DB
        self.assertIsNotNone(DB)
        self.assertIsInstance(DB, SQLAlchemy)
        self.assertTrue(hasattr(test_flask_app, 'DB'))
        self.assertIsInstance(test_flask_app.DB, SQLAlchemy)

    def test_get_sql_db_not_load_sqlalchemy_when_configured_accordingly(self):
        test_flask_app = Flask(
            "base.test_app",
            instance_path=(prefix + '/config/'),
            instance_relative_config=True,
            static_folder='public')

        test_flask_app.config["PACKAGE_SQLALCHEMY_ENABLED"] = False
        _init_sql_db(test_flask_app)
        self.assertFalse(hasattr(test_flask_app, 'DB'))

    def test_registered_blueprints(self):
        flask_app = create_app(package_name="base.app")
        app_blueprints = [name for name in flask_app.blueprints.keys()]
        for blueprint in blueprints:
            self.assertTrue(blueprint.name in app_blueprints)

    def test_register_app_loggers_when_rotating_filelogger_output_location_not_set(self):
        test_flask_app = Flask(
            "base.test_app",
            instance_path=(prefix + '/config/'),
            instance_relative_config=True,
            static_folder='public')
        test_flask_app.basepath = "./"
        test_flask_app.config["ROTATING_FILELOGGER_OUTPUT_LOCATION"] = None
        _register_app_loggers(test_flask_app)
        self.assertEquals(1, len(test_flask_app.logger.handlers))
        self.assertNotIsInstance(test_flask_app.logger.handlers[0], FileHandler)

    def test_register_app_loggers_when_rotating_filelogger_output_location_set(self):
        test_flask_app = Flask(
            "base.test_app",
            instance_path=(prefix + '/config/'),
            instance_relative_config=True,
            static_folder='public')
        test_flask_app.basepath = _get_basepath(test_flask_app)
        test_flask_app.config["ROTATING_FILELOGGER_OUTPUT_LOCATION"] = "logs/test.json"
        _register_app_loggers(test_flask_app)
        self.assertIsInstance(test_flask_app.logger.handlers[1], FileHandler)
