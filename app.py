from flask import Flask
from views import test
import config
from modules.post_info import post_info, db

app = Flask(__name__)
# register blueprint
app.register_blueprint(test.test)
app.register_blueprint(post_info)
# load config file
app.config.from_object(config)
db.init_app(app)


if __name__ == '__main__':
    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()
    app.run(debug=True)