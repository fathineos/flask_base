from setuptools import setup, find_packages


setup(name="base",
      packages=find_packages(),
      version="0.1.44",
      description="flask framework utility library",
      author="Fotis Athinaios",
      author_email="fotis.athineos@gmail.com",
      url="github.com/fathineos/flask_base",
      long_description="",
      install_requires=["alembic", "Flask", "Flask-Script",
                        "Flask-SQLAlchemy", "iso8601", "MySQL-python",
                        "iso8601", "python-json-logger","pytz",
                        "SQLAlchemy"])
