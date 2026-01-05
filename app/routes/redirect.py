from datetime import datetime
from flask import Blueprint, request, redirect, abort, current_app
from app.models.link import Link, AccessLog
from app import db
from app.services.cache import cache

redirect_bp = Blueprint('redirect', __name__)

@redirect_bp.route('/<short_code>')
def handle_redirect(short_code):
    # Try cache first
    cached_url = cache.get_link(short_code)
    if cached_url:
        # We still need to log the click if we use cache
        # For now, let's just query the DB for the link object to get its ID
        link = Link.query.filter_by(short_code=short_code, is_active=True).first()
    else:
        link = Link.query.filter_by(short_code=short_code, is_active=True).first()
        if link:
            cache.set_link(short_code, link.original_url)

    if not link:
        abort(404)
        
    if link.expires_at and link.expires_at < datetime.utcnow():
        link.is_active = False
        db.session.commit()
        cache.invalidate(short_code)
        abort(410)
    
    ua = request.headers.get('User-Agent', '')
    log = AccessLog(
        link_id=link.id,
        ip_address=request.remote_addr,
        user_agent=ua, 
        browser="Chrome" if "Chrome" in ua else "Safari" if "Safari" in ua else "Firefox" if "Firefox" in ua else "Other",
        os="Windows" if "Windows" in ua else "Mac" if "Mac" in ua else "Linux" if "Linux" in ua else "Other",
        device="Mobile" if "Mobile" in ua else "Desktop"
    )
    db.session.add(log)
    db.session.commit()
    
    current_app.logger.info(f"Redirected {short_code} to {link.original_url}")
    return redirect(link.original_url)
