from flask import Blueprint

test = Blueprint('test', __name__, url_prefix='/test')

@test.route('/')
def hello_world():
    return 'Hello world!'