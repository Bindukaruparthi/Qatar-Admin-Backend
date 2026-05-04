from flask import Blueprint, request
from models import db, Admin
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()

@auth_bp.route("/signup", methods=["POST"])
def signup():
    print(request.json)
    
    data = request.json

    if not all([data.get("full_name"), data.get("email"), data.get("password"), data.get("confirm_password")]):
        return {"error": "All fields required"}, 400

    if data["password"] != data["confirm_password"]:
        return {"error": "Passwords do not match"}, 400

    if len(data["password"]) < 8:
        return {"error": "Password must be 8+ chars"}, 400

    existing = Admin.query.filter_by(email=data["email"]).first()
    if existing:
        return {"error": "Account already exists"}, 400

    hashed = bcrypt.generate_password_hash(data["password"]).decode()

    admin = Admin(
        full_name=data["full_name"],
        email=data["email"],
        password=hashed
    )

    db.session.add(admin)
    db.session.commit()

    return {"message": "Signup successful"}, 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    admin = Admin.query.filter_by(email=data["email"]).first()

    if not admin or not bcrypt.check_password_hash(admin.password, data["password"]):
        return {"error": "Invalid email or password"}, 401

    token = create_access_token(identity=str(admin.id))

    return {"token": token}, 200