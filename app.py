from flask import Flask
from config import Config
from models import db
from routes.auth import auth_bp
from routes.opportunities import opp_bp
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS

print("SERVER STARTED")

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
CORS(app)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(opp_bp, url_prefix="/opportunities")

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return {"message": "Backend running"}

if __name__ == "__main__":
    app.run(debug=True)