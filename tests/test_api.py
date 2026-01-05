import pytest
from app import create_app, db
from app.models.user import User
from app.models.link import Link
import json

@pytest.fixture
def app():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test-secret'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_header(client):
    # Register and login to get token
    client.post('/api/auth/register', json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    response = client.post('/api/auth/login', json={
        "email": "test@example.com",
        "password": "password123"
    })
    token = response.get_json()['access_token']
    return {"Authorization": f"Bearer {token}"}

def test_register_and_login(client):
    reg_resp = client.post('/api/auth/register', json={
        "username": "newuser",
        "email": "new@example.com",
        "password": "password123"
    })
    assert reg_resp.status_code == 201

    login_resp = client.post('/api/auth/login', json={
        "email": "new@example.com",
        "password": "password123"
    })
    assert login_resp.status_code == 200
    assert "access_token" in login_resp.get_json()

def test_create_link_validation(client, auth_header):
    # Missing original_url
    resp = client.post('/api/links', json={"title": "Test"}, headers=auth_header)
    assert resp.status_code == 422
    assert "original_url" in resp.get_json()['original_url']

    # Invalid URL
    resp = client.post('/api/links', json={"original_url": "not-a-url"}, headers=auth_header)
    assert resp.status_code == 422

def test_link_lifecycle(client, auth_header):
    # 1. Create Link
    create_resp = client.post('/api/links', json={
        "original_url": "https://google.com",
        "title": "Google",
        "tag": "search"
    }, headers=auth_header)
    assert create_resp.status_code == 201
    link_data = create_resp.get_json()
    short_code = link_data['short_code']
    link_id = link_data['id']

    # 2. Redirect (Log access)
    redir_resp = client.get(f'/{short_code}')
    assert redir_resp.status_code == 302
    assert redir_resp.location == "https://google.com"

    # 3. Check Stats
    stats_resp = client.get(f'/api/analytics/{link_id}/stats', headers=auth_header)
    assert stats_resp.status_code == 200
    stats = stats_resp.get_json()
    assert stats['total_clicks'] == 1
    assert "Google" in stats['link']['title']

def test_admin_global_stats(client, auth_header, app):
    # Regular user fails
    resp = client.get('/api/analytics/global', headers=auth_header)
    assert resp.status_code == 401 # UnauthorizedError raised for non-admin

    # Promote to admin
    with app.app_context():
        user = User.query.filter_by(email="test@example.com").first()
        user.role = 'admin'
        db.session.commit()

    resp = client.get('/api/analytics/global', headers=auth_header)
    assert resp.status_code == 200
    assert "total_links" in resp.get_json()
