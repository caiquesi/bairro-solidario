import datetime
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="ONG Bairro Solidário")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Banco de dados fictício em memória para simular a persistência
# Banco de dados fictício expandido para simular mais de 30 itens na listagem
estoque_db = [
    {"id": 1, "nome": "Arroz Integral Camil", "quantidade": 150, "categoria": "Alimentos", "data_validade": "2027-08-30"},
    {"id": 2, "nome": "Leite UHT Integral", "quantidade": 50, "categoria": "Alimentos", "data_validade": "2026-11-20"}, # Alerta Crítico
    {"id": 3, "nome": "Feijão Carioca Kicaldo", "quantidade": 120, "categoria": "Alimentos", "data_validade": "2027-04-15"},
    {"id": 4, "nome": "Macarrão Espaguete Galo", "quantidade": 200, "categoria": "Alimentos", "data_validade": "2027-09-10"},
    {"id": 5, "nome": "Óleo de Soja Liza", "quantidade": 85, "categoria": "Alimentos", "data_validade": "2027-02-28"},
    {"id": 6, "nome": "Açúcar Refinado Caravelas", "quantidade": 90, "categoria": "Alimentos", "data_validade": "2027-06-18"},
    {"id": 7, "nome": "Sal Refinado Cisne", "quantidade": 40, "categoria": "Alimentos", "data_validade": "2028-01-05"},
    {"id": 8, "nome": "Café Torrado Pilão", "quantidade": 65, "categoria": "Alimentos", "data_validade": "2027-03-22"},
    {"id": 9, "nome": "Farinha de Trigo Dona Benta", "quantidade": 110, "categoria": "Alimentos", "data_validade": "2027-05-14"},
    {"id": 10, "nome": "Sabonete Rexona 90g", "quantidade": 300, "categoria": "Higiene", "data_validade": "2028-05-20"},
    {"id": 11, "nome": "Creme Dental Colgate", "quantidade": 250, "categoria": "Higiene", "data_validade": "2028-03-12"},
    {"id": 12, "nome": "Shampoo Seda Ceramidas", "quantidade": 140, "categoria": "Higiene", "data_validade": "2028-02-18"},
    {"id": 13, "nome": "Papel Higiênico Neve 4un", "quantidade": 180, "categoria": "Higiene", "data_validade": "2029-12-31"},
    {"id": 14, "nome": "Detergente Líquido Ypê", "quantidade": 95, "categoria": "Higiene", "data_validade": "2027-11-05"},
    {"id": 15, "nome": "Sabão em Pó Omo 1kg", "quantidade": 70, "categoria": "Higiene", "data_validade": "2027-10-25"},
    {"id": 16, "nome": "Desinfetante Pinho Sol", "quantidade": 60, "categoria": "Higiene", "data_validade": "2027-08-14"},
    {"id": 17, "nome": "Água Sanitária Ypê 1L", "quantidade": 80, "categoria": "Higiene", "data_validade": "2027-07-19"},
    {"id": 18, "nome": "Agasalho de Lã Adulto", "quantidade": 45, "categoria": "Vestuário", "data_validade": "2035-12-31"},
    {"id": 19, "nome": "Calça Jeans Masculina", "quantidade": 55, "categoria": "Vestuário", "data_validade": "2035-12-31"},
    {"id": 20, "nome": "Camiseta de Algodão", "quantidade": 115, "categoria": "Vestuário", "data_validade": "2035-12-31"},
    {"id": 21, "nome": "Casaco Infantil Moletom", "quantidade": 35, "categoria": "Vestuário", "data_validade": "2035-12-31"},
    {"id": 22, "nome": "Manta de Microfibra Casal", "quantidade": 42, "categoria": "Vestuário", "data_validade": "2035-12-31"},
    {"id": 23, "nome": "Fubá Mimoso Granfino", "quantidade": 75, "categoria": "Alimentos", "data_validade": "2027-04-30"},
    {"id": 24, "nome": "Farinha de Mesa Mandioca", "quantidade": 60, "categoria": "Alimentos", "data_validade": "2027-06-01"},
    {"id": 25, "nome": "Extrato de Tomate Elefante", "quantidade": 130, "categoria": "Alimentos", "data_validade": "2027-08-22"},
    {"id": 26, "nome": "Sardinha em Lata Coqueiro", "quantidade": 160, "categoria": "Alimentos", "data_validade": "2028-02-15"},
    {"id": 27, "nome": "Ervilha em Conserva Quero", "quantidade": 145, "categoria": "Alimentos", "data_validade": "2027-10-10"},
    {"id": 28, "nome": "Milho Verde em Lata Quero", "quantidade": 150, "categoria": "Alimentos", "data_validade": "2027-11-20"},
    {"id": 29, "nome": "Biscoito Cream Cracker Vitarella", "quantidade": 190, "categoria": "Alimentos", "data_validade": "2027-03-15"},
    {"id": 30, "nome": "Achocolatado em Pó Nescau", "quantidade": 85, "categoria": "Alimentos", "data_validade": "2027-05-25"},
    {"id": 31, "nome": "Vinagre de Álcool Castelo", "quantidade": 50, "categoria": "Alimentos", "data_validade": "2027-09-30"},
    {"id": 32, "nome": "Esponja de Aço Assolan", "quantidade": 220, "categoria": "Higiene", "data_validade": "2029-01-01"}
]

coletas_db = [
    {"id": 1, "nome_doador": "Marcos Silva", "telefone": "11999999999", "endereco": "Rua Principal, 123", "item": "Guarda-roupa", "status": "Confirmado"},
    {"id": 2, "nome_doador": "Ana Oliveira", "telefone": "11988888888", "endereco": "Av Central, 456", "item": "Mesa com 4 cadeiras", "status": "Pendente"},
    {"id": 3, "nome_doador": "Ricardo Santos", "telefone": "11977777777", "endereco": "Rua das Flores, 789", "item": "Sofá 3 lugares", "status": "Confirmado"},
    {"id": 4, "nome_doador": "Cláudia Lima", "telefone": "11966666666", "endereco": "Alameda Norte, 102", "item": "Fogão 4 bocas", "status": "Concluído"},
    {"id": 5, "nome_doador": "Roberto Souza", "telefone": "11955555555", "endereco": "Rua Silva, 55", "item": "Cama de Solteiro", "status": "Pendente"}
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
