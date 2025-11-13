from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from routes.auth_routes import auth
from flask_login import LoginManager
from models import get_user_by_id
from routes.plans_routes import plans_bp
from routes.favorites_routes import  favorites_bp
from routes.exercises_routes import  exercises_bp

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, supports_credentials=True, origins=["https://localhost:3000"])
#CORS(
 #   app,
  #  resources={r"/*": {"origins": ["http://127.0.0.1:3000"]}},
   # supports_credentials=True,
#)

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(plans_bp, url_prefix='/plans_bp')
app.register_blueprint(favorites_bp, url_prefix='/favorites')
app.register_blueprint(exercises_bp, url_prefix='/api')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = None

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

@login_manager.unauthorized_handler
def unauthorized_callback():
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/')
def home():
    return {"message": "it works!"}

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, port = 8080)