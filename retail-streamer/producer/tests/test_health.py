def test_health(test_app):
    response = test_app.get('/health')
    assert response.status_code == 200
