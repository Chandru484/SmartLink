import random
import string
import validators
from app.models.link import Link
from app import db

class LinkService:
    @staticmethod
    def generate_short_code(length=6):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    def create_link(user_id, original_url, title=None, custom_alias=None, expires_at=None, tag=None):
        if '://' not in original_url:
            original_url = 'http://' + original_url
            
        if not validators.url(original_url):
            raise ValueError("Invalid destination URL")
            
        code = custom_alias or LinkService.generate_short_code()
        
        if Link.query.filter_by(short_code=code).first():
            raise ValueError("Alias taken")
            
        link = Link(
            original_url=original_url,
            short_code=code,
            title=title,
            tag=tag,
            user_id=user_id,
            expires_at=expires_at
        )
        db.session.add(link)
        db.session.commit()
        return link
