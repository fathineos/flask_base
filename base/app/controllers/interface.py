"""
Simple example of controller
"""

from flask import Blueprint
from base.app.controllers import accepts_mimetypes


interface = Blueprint('interface', __name__, url_prefix='/')


@interface.route('/', methods=['GET'])
@accepts_mimetypes(supported_types=["application/json"])
def index():
    return 'This is a example controller.', 203
