from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models.user import User
from app.schemas import UserRegisterSchema
from app import db
from marshmallow import ValidationError

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = UserRegisterSchema().load(request.get_json())
    except ValidationError as e:
        return jsonify({"msg": "Validation failed", "errors": e.messages}), 422
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"msg": "Email exists"}), 400
    
    u = User(username=data['username'], email=data['email'])
    u.set_password(data['password'])
    db.session.add(u)
    db.session.commit()
    return jsonify({"msg": "User created"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    d = request.get_json()
    u = User.query.filter_by(email=d.get('email')).first()
    if not u or not u.check_password(d.get('password')):
        return jsonify({"msg": "Invalid credentials"}), 401
    
    return jsonify({
        "access_token": create_access_token(identity=str(u.id)),
        "user": u.to_dict()
    })
