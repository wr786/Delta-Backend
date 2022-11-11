from flask import Flask,session
from views import test
import config
from modules.post_info import post_info, db
from modules.login_regist.login import login_blue
from modules.login_regist.regist import regist_blue
from modules.login_regist.getsesinfo import getsesinfo_blue
from modules.login_regist.logout import logout_blue

app = Flask(__name__)
app.secret_key=config.SECRET_KEY
# register blueprint
app.register_blueprint(test.test)
app.register_blueprint(post_info)
app.register_blueprint(login_blue)
app.register_blueprint(regist_blue)
app.register_blueprint(getsesinfo_blue)
app.register_blueprint(logout_blue)
# load config file
app.config.from_object(config)
db.init_app(app)


if __name__ == '__main__':
    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()
    app.run(debug=True)