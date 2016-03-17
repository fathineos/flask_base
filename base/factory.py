"""The module responsible to create the application with the appropriate
configuration and register all the necessary submodules. The application runs
in standalone (native) mode or as a library. Initializes all submodules
required by the application such as database instances, blueprints etc."""

from sys import prefix
from os.path import join, abspath, dirname
from os import environ
from logging import DEBUG
from flask import Flask
from werkzeug.exceptions import default_exceptions
from pythonjsonlogger import jsonlogger
from logging.handlers import RotatingFileHandler


DB = None

ENVIRONMENT_PRODUCTION = "production"
ENVIRONMENT_DEVELOPMENT = "development"
ENVIRONMENT_TESTING = "testing"
BASE_MODE_LIBRARY = "MODE_LIBRARY"
BASE_MODE_NATIVE = "MODE_NATIVE"


def create_app(package_name, basepath=None, forced_environment=None):
    """
    The application factory where the flask application bootstraps. Creates a
    flask application object and configures it with all required parameters and
    configuratiob, according to the current environment passed as parameter to
    the factory. The application is instantiated in with sigleton pattern.

    :param package_name: the name of the root package of the application
    instance to create
    :param basepath: A full path to the source of the application
    :param forced_environment: The environment the app should bootstrap with
    :type basepath: str
    :type package_name: str
    :type forced_environment:  str
    :return: The flask application object
    :rtype: flask.app.Flask
    """

    app = Flask(
        package_name,
        instance_path=(prefix + "/config/"),
        instance_relative_config=True,
        static_folder="public")

    if basepath:
        app.base_mode = BASE_MODE_LIBRARY
    else:
        app.base_mode = BASE_MODE_NATIVE

    _get_basepath(app, forced_basepath=basepath)

    _app_configs(app, forced_environment)
    _register_app_loggers(app)
    _register_additional_packages(app)
    _register_exception_error_handler(app)
    from base.app.controllers.front_controller import blueprints
    _register_blueprints(app, blueprints)
    return app


def _get_basepath(app, forced_basepath=None):
    if forced_basepath:
        app.basepath = forced_basepath
    else:
        app.basepath = abspath(dirname(__file__))
    return app.basepath


def _register_app_loggers(app):
    """Register application loggers handlers. Log level is debug, so info,
    warning and error will be logged in a uniform JSON format. By default the
    logs are output to stdout, if the param ROTATING_FILELOGGER_OUTPUT_LOCATION
    is set, then all logs will be also output in the specified filepath.
    If app is running in debug mode, flask will register a log handler which
    outputs to stdout. Other submodules may also register custom log hanlders.

    :param app: The flask application object
    :type app: flask.app.Flask
    """
    app.logger.setLevel(DEBUG)
    log_path = app.config.get("ROTATING_FILELOGGER_OUTPUT_LOCATION")

    if log_path:
        absolute_log_path = "{}/../{}".format(app.basepath, log_path)
        file_log_handler = _rotating_file_logger(absolute_log_path)
        app.logger.addHandler(file_log_handler)

    for handler in app.logger.handlers:
        handler.setFormatter(_json_log_formatter())


def _rotating_file_logger(file_log_path):
    """Get a flask Rotating File Handler log handler

    :param file_log_path: The absolute path to log file
    :type file_log_path: str
    """
    log_handler = RotatingFileHandler(file_log_path,
                                      maxBytes=10000,
                                      backupCount=1)
    return log_handler


def _json_log_formatter():
    """Get json formatter for log handlers"""
    formatter = jsonlogger.JsonFormatter(
        '%(asctime) %(levelname) %(module) %(funcName) %(lineno) %(message)')
    return formatter


def _app_configs(app, forced_environment=None):
    """Initialize application configuration based on environment. Combines the
    default configuration with environmental specific

    :param app: The flask application object
    :param forced_environment: A string denoting the environment we force the
    application to bootstrap with
    :type app: flask.app.Flask
    :type forced_environment: str
    """
    from base.app.configs import default
    app.config.from_object(default)

    if app.base_mode == BASE_MODE_LIBRARY:
        config_file_path = join(app.basepath, "app/configs/default.py")
        app.config.from_pyfile(config_file_path, silent=True)

    _get_environment(app, forced_environment, app.basepath)
    config_file_path = join(app.basepath, "app/configs/{}.py".format(app.env))
    app.config.from_pyfile(config_file_path, silent=True)


def _get_environment(app, forced_environment, basepath):
    environment_variable = environ.get("APPLICATION_ENV")
    if environment_variable:
        env = environment_variable
    elif forced_environment:
        env = forced_environment
    else:
        application_id_path = app.config.get("APPLICATION_ID_PATH")
        with open(join(basepath, application_id_path)) as appid:
            env = appid.read().strip()
    app.env = env
    return env


def _register_blueprints(app, blueprints):
    """Registers app blueprints. A blueprint defines a collection of views,
    templates, static files and other elements that can be applied to an
    application.
    TODO: Should become public, since called when base is run in library mode.

    :param app: The flask application object
    :type app: flask.app.Flask
    :param blueprints
    :type blueprints: flask.Blueprint
    """
    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def _register_exception_error_handler(app):
    """Register exception handler to handle http exceptions and generic
    exceptions and return a api response, that follows the standard envelope.

    :param app: The flask application object
    :type app: flask.app.Flask
    """
    from base.exception_handler import exception_handler
    for exception in default_exceptions:
        app.register_error_handler(exception, exception_handler)

    app.register_error_handler(Exception, exception_handler)


def _register_additional_packages(app):
    """Register optional packages on runtime, which should be enabled/disabled
    from configuration.

    :param app: The flask application object
    :type app: flask.app.Flask
    """
    _init_sql_db(app)


def _init_sql_db(app):
    """Configurable registeration of SqlAlchemy package.

    :param app: The flask application object
    :type app: flask.app.Flask
    """
    if app.config.get("PACKAGE_SQLALCHEMY_ENABLED"):
        global DB
        if DB is None:
            from flask_sqlalchemy import SQLAlchemy
            DB = SQLAlchemy()
            DB.init_app(app)
            DB.app = app

        app.DB = DB
