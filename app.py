from flask import Flask
from views import test

app = Flask(__name__)
app.register_blueprint(test.test)

if __name__ == '__main__':
    app.run(debug=True)