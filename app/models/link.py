from datetime import datetime
from app import db

class Link(db.Model):
    __tablename__ = 'links'
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.Text, nullable=False)
    short_code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    title = db.Column(db.String(200))
    tag = db.Column(db.String(50), nullable=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    expires_at = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    logs = db.relationship('AccessLog', backref='link', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id, "original_url": self.original_url, "short_code": self.short_code,
            "title": self.title, "tag": self.tag, "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "is_active": self.is_active, "click_count": len(self.logs)
        }

class AccessLog(db.Model):
    __tablename__ = 'access_logs'
    id = db.Column(db.Integer, primary_key=True)
    link_id = db.Column(db.Integer, db.ForeignKey('links.id'), nullable=False, index=True)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(255))
    referer = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    browser = db.Column(db.String(50))
    os = db.Column(db.String(50))
    device = db.Column(db.String(50))
