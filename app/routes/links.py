import random
import string
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.link import Link
from app.schemas import LinkCreateSchema
from app import db
from marshmallow import ValidationError

from app.services.link_service import LinkService

links_bp = Blueprint('links', __name__, url_prefix='/api/links')

@links_bp.route('', methods=['POST'])
@jwt_required()
def create_link():
    try:
        d = LinkCreateSchema().load(request.get_json())
    except ValidationError as e:
        from flask import current_app
        current_app.logger.warning(f"Validation failed: {e.messages} | Data: {request.get_json()}")
        return jsonify({"msg": "Validation failed", "errors": e.messages}), 422
    
    try:
        l = LinkService.create_link(
            user_id=int(get_jwt_identity()),
            original_url=d['original_url'],
            title=d.get('title'),
            custom_alias=d.get('custom_alias'),
            expires_at=d.get('expires_at'),
            tag=d.get('tag')
        )
        return jsonify(l.to_dict()), 201
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400

@links_bp.route('', methods=['GET'])
@jwt_required()
def get_user_links():
    links = Link.query.filter_by(user_id=int(get_jwt_identity())).order_by(Link.created_at.desc()).all()
    return jsonify({"links": [l.to_dict() for l in links]})

@links_bp.route('/<int:link_id>', methods=['GET'])
@jwt_required()
def get_link(link_id):
    link = Link.query.get_or_404(link_id)
    if link.user_id != int(get_jwt_identity()):
        abort(403)
    return jsonify(link.to_dict())

@links_bp.route('/<int:link_id>', methods=['PUT'])
@jwt_required()
def update_link(link_id):
    link = Link.query.get_or_404(link_id)
    if link.user_id != int(get_jwt_identity()):
        abort(403)
    
    data = request.get_json()
    link.title = data.get('title', link.title)
    link.tag = data.get('tag', link.tag)
    link.is_active = data.get('is_active', link.is_active)
    
    db.session.commit()
    return jsonify(link.to_dict())

@links_bp.route('/<int:link_id>', methods=['DELETE'])
@jwt_required()
def delete_link(link_id):
    link = Link.query.get_or_404(link_id)
    if link.user_id != int(get_jwt_identity()):
        abort(403)
    
    db.session.delete(link)
    db.session.commit()
    return jsonify({"msg": "Link deleted"})
