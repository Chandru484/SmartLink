import pytest
from app import create_app, db
from app.models.user import User
from app.services.link_service import LinkService

@pytest.fixture
def app():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_short_code_generation(app):
    with app.app_context():
        code1 = LinkService.generate_short_code(6)
        code2 = LinkService.generate_short_code(6)
        assert len(code1) == 6
        assert code1 != code2

def test_link_validation(app):
    with app.app_context():
        with pytest.raises(Exception): # ValidationError
            LinkService.create_link(1, "not-a-url")
