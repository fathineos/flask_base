"""
Simple example of controller
"""

from flask import Blueprint


interface = Blueprint('interface', __name__, url_prefix='/')


@interface.route('/', methods=['GET'])
def index():
    return 'This is a example controller.'
