from sys import prefix
from flask import Flask
from os.path import abspath, dirname, join

DB = None

ENVIRONMENT_PRODUCTION = "production"
ENVIRONMENT_DEVELOPMENT = "development"
ENVIRONMENT_TESTING = "testing"

BASEPATH = abspath(dirname(__file__))

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

    _app_configs(app, forced_environment)
    _register_blueprints(app)
    _register_additional_packages(app)
    return app


def _app_configs(app, forced_environment):
    """Initialize application configuration based on environment. Combines the
    default configuration with environmental specific

    :param app: The flask application object
    :type app: flask.app.Flask
    :param forced_environment: A string denoting the environment we force the
    application to bootstrap with
    :type forced_environment: str
    """

    from base.app.configs import default
    app.config.from_object(default)

    app.environment = _get_environment(app, forced_environment)
    config_file_path = join(BASEPATH, "app/configs/{}.py".format(app.environment))
    app.config.from_pyfile(config_file_path, silent=True)


def _get_environment(app, forced_environment):
    if forced_environment:
        return forced_environment

    from os import environ
    environment_variable = environ.get("APPLICATION_ENV")
    if environment_variable:
        return environment_variable

    application_id_path = app.config.get("APPLICATION_ID_PATH")
    with open(join(BASEPATH, application_id_path)) as appid:
        env = appid.read().strip()

    return env


def _register_blueprints(app):
    from base.app.front_controller import blueprints
    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def _register_additional_packages(app):
    _init_sql_db(app)


def _init_sql_db(app):
    if app.config.get("PACKAGE_SQLALCHEMY_ENABLED"):
        global DB
        if DB is None:
            from flask_sqlalchemy import SQLAlchemy
            DB = SQLAlchemy()
            DB.init_app(app)
            DB.app = app

        app.DB = DB
