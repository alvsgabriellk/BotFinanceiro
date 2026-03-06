import json

CAMINHO_ARQUIVO_FINANCEIRO = "data/dados_financeiros.json"

def carregar_dados():
    with open(CAMINHO_ARQUIVO_FINANCEIRO, "r") as f:
        return json.load(f)
    
def salvar_dados(dados):
    with open(CAMINHO_ARQUIVO_FINANCEIRO, "w") as f:
        return json.dump(CAMINHO_ARQUIVO_FINANCEIRO, f, indent=4)
    

def definirSalario(mes, valor):
    dados = carregar_dados()

    if mes not in dados:
        dados[mes] = {
            "salario_base": 0,
            "rendas_extras": [],
            "limite_mensal": 0
        }

        dados[mes]["salario_base"] = valor

        salvar_dados(dados)

    
