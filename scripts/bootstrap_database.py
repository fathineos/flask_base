import sys
from flask import Flask
from sqlalchemy import create_engine
from base.factory import _app_configs, _get_basepath


try:
    app_module = sys.argv[1]
except IndexError:
    print "Error: application app module not provided!"
    exit(1)

app = Flask(app_module)
_app_configs(app, None, _get_basepath())
db_name = app.config["SQLALCHEMY_DATABASE_URI"].split("/")[-1:][0]
if (app.config["PACKAGE_SQLALCHEMY_ENABLED"] == True):
    mysql_uri = app.config["SQLALCHEMY_DATABASE_URI"].replace(db_name, "")
    engine = create_engine(mysql_uri)
    engine.execute("CREATE DATABASE IF NOT EXISTS " + db_name)
    print "Created database {}".format(db_name)
