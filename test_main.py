from fastapi.testclient import TestClient
from main import app, estoque_db

client = TestClient(app)

# Teste 1: Valida se a Tela 1 (Dashboard) carrega com sucesso
def test_read_dashboard():
    response = client.get("/")
    assert response.status_code == 200
    assert "Painel de Controle Principal" in response.text

# Teste 2: Valida se a Tela 2 (Formulário) carrega com sucesso
def test_view_cadastro():
    response = client.get("/cadastro")
    assert response.status_code == 200
    assert "Triagem de Insumos" in response.text

# Teste 3: Valida a regra de negócio de cadastro válido com sucesso (RF01)
def test_salvar_insumo_sucesso():
    dados = {
        "nome": "Suco de Uva",
        "quantidade": 10,
        "categoria": "Alimentos",
        "data_validade": "2027-12-31"
    }
    response = client.post("/cadastro/salvar", data=dados, follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/listagem"

# Teste 4: Valida se o sistema bloqueia quantidade menor ou igual a zero (Regra de Negócio)
def test_salvar_insumo_quantidade_invalida():
    dados = {
        "nome": "Feijão",
        "quantidade": 0,
        "categoria": "Alimentos",
        "data_validade": "2027-12-31"
    }
    response = client.post("/cadastro/salvar", data=dados, follow_redirects=False)
    assert response.status_code == 303
    assert "erro=" in response.headers["location"]

# Teste 5: Valida se a Tela 3 (Listagem Geral) renderiza os dados perfeitamente
def test_read_listagem():
    response = client.get("/listagem")
    assert response.status_code == 200
    assert "Inventário de Estoque Atualizado" in response.text
