from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from auth_routes import auth
from flask_login import LoginManager
from models import get_user_by_id, User
from plans_routes import plans_bp

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, supports_credentials=True)

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(plans_bp)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

@app.route('/')
def home():
    return {"message": "it works!"}

if __name__ == '__main__':
    app.run(debug=True)