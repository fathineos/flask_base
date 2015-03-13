"""Front Controller is used to collect all application Blueprints, which will
be registered to app in factory on app initialization
"""

from base.app.controllers.interface import interface

blueprints = [interface]
