from base.app import create
from flask.ext.script import Manager

app = create()
app.debug = True
manager = Manager(app)


if __name__ == '__main__':
    manager.run()
