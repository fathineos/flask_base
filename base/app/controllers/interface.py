"""Absolute minimum service endpoints"""

from flask import Blueprint


interface = Blueprint('interface', __name__)


@interface.route('/health', methods=['GET'])
def index():
    return 'Service is up', 200
