import pytest

@pytest.mark.skip # TEMP for speed
def test_availability(app, client):
    @app.get('/')
    def index(): return ''

    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == ''

