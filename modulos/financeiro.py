import json
import os

CAMINHO_ARQUIVO_FINANCEIRO = "data/dados_financeiros.json"

def carregar_dados():
    if not os.path.exists(CAMINHO_ARQUIVO_FINANCEIRO):
        return dict()
    if os.path.getsize(CAMINHO_ARQUIVO_FINANCEIRO) == 0:
        return dict()

    with open(CAMINHO_ARQUIVO_FINANCEIRO, "r") as f:
        return json.load(f)
    
def salvar_dados(dados):
    with open(CAMINHO_ARQUIVO_FINANCEIRO, "w") as f:
        json.dump(dados, f, indent=4)
    

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

def adicionarRendaExtra(mes, valor):
    dados = carregar_dados()

    if mes not in dados:
        return "Mês não encontrado."
    dados[mes]["rendas_extras"].append(valor)

    salvar_dados(dados)


def definirLimite(mes, valor):
    dados = carregar_dados()
    
    if mes not in dados:
        return "Mês não encontrado."
    dados[mes]["limite_mensal"] = valor

    salvar_dados(dados)
