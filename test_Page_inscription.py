import pytest
from Page_inscription import app  # Importation de ton application Flask

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_login_page(client):
    """Test si la page de login s'affiche correctement."""
    response = client.get('/login')
    assert response.status_code == 200
    assert b"Identifiez-vous" in response.data  # Vérifie si la page contient le texte "Identifiez-vous"

def test_create_account_page(client):
    """Test si la page de création de compte s'affiche correctement."""
    response = client.get('/create-account')
    assert response.status_code == 200
    assert "Créez un compte" in response.data
