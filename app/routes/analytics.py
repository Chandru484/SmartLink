import io
import pandas as pd
from flask import Blueprint, jsonify, Response, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.link import Link, AccessLog
from app.models.user import User

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')

@analytics_bp.route('/global', methods=['GET'])
@jwt_required()
def global_stats():
    return jsonify({
        "total_links": Link.query.count(),
        "total_clicks": AccessLog.query.count()
    })

@analytics_bp.route('/user', methods=['GET'])
@jwt_required()
def user_stats():
    user_id = int(get_jwt_identity())
    links = Link.query.filter_by(user_id=user_id).all()
    link_ids = [l.id for l in links]
    total_clicks = AccessLog.query.filter(AccessLog.link_id.in_(link_ids)).count() if link_ids else 0
    return jsonify({
        "total_links": len(links),
        "total_clicks": total_clicks
    })

@analytics_bp.route('/<int:link_id>/stats', methods=['GET'])
@jwt_required()
def link_stats(link_id):
    link = Link.query.get_or_404(link_id)
    if link.user_id != int(get_jwt_identity()):
        abort(403)
    
    return jsonify({
        "link": link.to_dict(),
        "total_clicks": len(link.logs)
    })

@analytics_bp.route('/<int:link_id>/export', methods=['GET'])
@jwt_required()
def export_stats(link_id):
    link = Link.query.get_or_404(link_id)
    if link.user_id != int(get_jwt_identity()):
        abort(403)
        
    logs = AccessLog.query.filter_by(link_id=link.id).all()
    if not logs:
        return jsonify({"msg": "No data to export"}), 404
        
    data = [{
        "Timestamp": log.timestamp,
        "IP Address": log.ip_address,
        "Browser": log.browser,
        "OS": log.os,
        "Device": log.device,
        "User Agent": log.user_agent
    } for log in logs]
    
    df = pd.DataFrame(data)
    output = io.BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-disposition": f"attachment; filename=stats_{link.short_code}.csv"}
    )
