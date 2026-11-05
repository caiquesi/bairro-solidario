import datetime
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="ONG Bairro Solidário")
templates = Jinja2Templates(directory="templates")

# Banco de dados fictício em memória para simular a persistência
estoque_db = [
    {"id": 1, "nome": "Arroz Integral", "quantidade": 150, "categoria": "Alimentos", "data_validade": "2027-08-30"},
    {"id": 2, "nome": "Leite UHT", "quantidade": 50, "categoria": "Alimentos", "data_validade": "2026-11-20"}, # Alerta
]

coletas_db = [
    {"id": 1, "nome_doador": "Marcos Silva", "telefone": "11999999999", "endereco": "Rua Principal, 123", "item": "Guarda-roupa", "status": "Confirmado"}
]

# Função utilitária para checar se o item vence em menos de 30 dias (RF02)
def checar_alerta(data_str):
    try:
        validade = datetime.datetime.strptime(data_str, "%Y-%m-%d").date()
        hoje = datetime.date.today()
        dias_restantes = (validade - hoje).days
        return 0 <= dias_restantes <= 30
    except ValueError:
        return False

# TELA 1: Entrada Principal / Dashboard
# TELA 1: Entrada Principal / Dashboard (Corrigido)
@app.get("/")
def read_dashboard(request: Request):
    alertas = [item for item in estoque_db if checar_alerta(item["data_validade"])]
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html", 
        context={"usuario": "Voluntário 01", "estoque": estoque_db, "alertas": alertas}
    )


# TELA 2: Formulário de Cadastro (Visualização)
@app.get("/cadastro")
def view_cadastro(request: Request, erro: str = None):
    return templates.TemplateResponse(
        request=request,
        name="formulario.html",
        context={"erro": erro}
    )


# TELA 2: Processamento do Formulário com Regras de Negócio (RF01)
@app.post("/cadastro/salvar")
def salvar_insumo(
    nome: str = Form(...), 
    quantidade: int = Form(...), 
    categoria: str = Form(...), 
    data_validade: str = Form(...)
):
    # Regra de Validação (Quantidade > 0 e Data Futura)
    hoje_str = datetime.date.today().strftime("%Y-%m-%d")
    if quantidade <= 0:
        return RedirectResponse(url="/cadastro?erro=A quantidade deve ser maior que zero.", status_code=303)
    if data_validade < hoje_str:
        return RedirectResponse(url="/cadastro?erro=A data de validade nao pode ser no passado.", status_code=303)
    
    # Inserção na persistência fictícia
    novo_id = len(estoque_db) + 1
    estoque_db.append({
        "id": novo_id,
        "nome": nome,
        "quantidade": quantidade,
        "categoria": categoria,
        "data_validade": data_validade
    })
    return RedirectResponse(url="/listagem", status_code=303)

# TELA 3: Listagem Geral e Resultados (RF03)
@app.get("/listagem")
def read_listagem(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="listagem.html",
        context={"estoque": estoque_db, "coletas": coletas_db}
    )


# Revisao de codigo efetuada para homologacao do MVP da ONG
