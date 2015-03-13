from base.factory import create_app


def create(basepath=None, forced_environment=None):
    """
    Instantiate and return flask app from factory

    :param environment: A string denoting the environment we would like the
    application to bootstrap with
    :type environment:  str
    :return: flask.app.Flask -- The flask application object created with
    corresponding configuration
    """
    return create_app(package_name=__name__,
                      basepath=basepath,
                      forced_environment=forced_environment)
