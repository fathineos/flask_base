from os import environ
from flask import Flask
from base.testing import TestCase
from base.factory import create_app, _get_environment, _init_sql_db,\
    ENVIRONMENT_DEVELOPMENT, ENVIRONMENT_TESTING


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
        result_env = _get_environment(flask_app,
                                      forced_environment=ENVIRONMENT_TESTING)
        self.assertEqual(ENVIRONMENT_TESTING, result_env)

    def test_get_application_env_when_os_environment_variable_is_not_set(self):
        flask_app = create_app(package_name="base.app")
        self.assertEqual(ENVIRONMENT_DEVELOPMENT,
                         _get_environment(flask_app, None))

    def test_get_application_env_when_os_environment_variable_is_set(self):
        flask_app = create_app(package_name="base.app")
        environ["APPLICATION_ENV"] = ENVIRONMENT_TESTING
        self.assertEqual(ENVIRONMENT_TESTING,
                         _get_environment(flask_app, None))

    def test_app_configs_registered_proper_configuration_packages(self):
        from sys import modules
        create_app(package_name="base.app",
                   forced_environment=ENVIRONMENT_TESTING)
        self.assertIn("base.app.configs.default", modules)
        self.assertIn("base.app.configs.testing", modules)

    def test_get_sql_db_load_sqlalchemy_package_when_configured_accordingly(self):
        from sys import prefix, modules
        from flask_sqlalchemy import SQLAlchemy

        test_flask_app = Flask(
            "base.test_app",
            instance_path=(prefix + '/config/'),
            instance_relative_config=True,
            static_folder='public'
        )

        test_flask_app.config["PACKAGE_SQLALCHEMY_ENABLED"] = True
        _init_sql_db(test_flask_app)
        self.assertIn("sqlalchemy", modules)
        from base.factory import DB
        self.assertIsNotNone(DB)
        self.assertIsInstance(DB, SQLAlchemy)
        self.assertTrue(hasattr(test_flask_app, 'DB'))
        self.assertIsInstance(test_flask_app.DB, SQLAlchemy)

    def test_get_sql_db_not_load_sqlalchemy_when_configured_accordingly(self):
        from sys import prefix
        test_flask_app = Flask(
            "base.test_app",
            instance_path=(prefix + '/config/'),
            instance_relative_config=True,
            static_folder='public'
        )

        test_flask_app.config["PACKAGE_SQLALCHEMY_ENABLED"] = False
        _init_sql_db(test_flask_app)
        self.assertFalse(hasattr(test_flask_app, 'DB'))
