from sys import prefix
from flask import Flask
from os.path import abspath, dirname


ENVIRONMENT_PRODUCTION = "production"
ENVIRONMENT_DEVELOPMENT = "development"
ENVIRONMENT_TESTING = "testing"

BASEPATH = abspath(dirname(__file__))
BASE_PACKAGE = None


def create_app(package_name, forced_environment=None):
    """
    Main application factory for the flask application bootstrap. Creates a
    flask application object and configures all its required parameters and
    settings according to the current environment passed as parameter to the
    factory. Initializes all singleton instances required by the application
    such as database instances, blueprints etc.

    :param package_name: the name of the root package of the application
    instance to create
    :type package_name: str
    :param package_path: the absolute path of the root package of the
    application instance to create
    :type package_path: str
    :param settings_override: A dictionary containing all setting keys to
    override with, after default bootstrap
    :type settings_override: dict
    :param environment: A string denoting the environment we would like the
    application to bootstrap with
    :type environment:  str
    :return: flask.app.Flask -- The flask application object created with
    corresponding configuration
    """

    app = Flask(
        package_name,
        instance_path=(prefix + '/config/'),
        instance_relative_config=True,
        static_folder='public'
    )

    _register_blueprints(app)
    return app


def _register_blueprints(app):
    from base.app.front_controller import blueprints
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
