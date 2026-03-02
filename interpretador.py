import re # encontra padrões / extrai dados / valida formatos
import os
import json

CAMINHO_ARQUIVO = "data/gastos.json"


def carregar_gastos():
    if not os.path.exists(CAMINHO_ARQUIVO):
        return []
    
    with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)
    















gastos = []

categorias = {
    "Alimentação": ["mercado", "restaurante", "lanche", "ifood", "salgado", "besteira", "bebida", "água", "comida"],
    "Transporte": ["uber", "ônibus"],
    "Pessoal": ["roupa", "acessório", "cabeleleiro", "cabelo", "academia"],
    "Presente": ["presente"],
    "Lazer": ["cinema", "passear", "jogo", "passeio", "crunchyroll", "evento", "corrida de rua", "praia"],
    "Financeiro": ["cartão de crédito", "empréstimo"],
    "Educação": ["curso", "livro", "faculdade"],
    "Saúde": ["farmácia", "remédio"],
    "Tecnologia": ["celular", "notebook", "hospedagem", "software", "equipamento"]
}

def detectar_categoria(text):
    for categoria, palavras in categorias.items():
        for palavra in palavras:
            if palavra in text:
                return categoria
    return "Outros"

def interpretar_mensagem(text):
    text = text.lower()

    comandosGastos = [
        "gastei",
        "comprei",
        "paguei",
        "parcelei",
        "comprar",
        "pagar",

        "eu paguei",
        "eu comprei",
        "eu fiz uma compra",
        "fiz uma compra",
        "eu gastei",
        "eu parcelei"
    ]
       #retorn true se apns um for tru        # percorre a lista toda
    if any(text.startswith(comando) for comando in comandosGastos):
        #text.starswith - verifica se começa com o comando


        #valorEncontrado = re.search(r"\d+", text) procura qualquer sequencia de números"""


        #if valorEncontrado:
            #valor = valorEncontrado.group()
            #return f"Entendi!, Você registrou um gasto de R${valor:.2f}

        if text.startswith("parcelei"):
            numeros = re.findall(r"\d+", text) # encontre todas sequencias de numeros no texto / + um ou mais

            if len(numeros) >= 2:
                parcelas = min(numeros, key=int)
                valorParcela = max(numeros, key=int)

                total = int(parcelas) * int(valorParcela)

                return (
                    f"Compra parcelada detectada!✅\n"
                    f"{parcelas}x de R${valorParcela}\n"
                    f"Total: R${total}"
                )
            return "Entendi que é parcelado, mas não identifiquei parcelas e valor corretamente"
        
        numeros = re.findall(r"\d+", text)

        if numeros:
            valor = max(numeros, key=int)

            categoria = detectar_categoria(text)

            gasto = {
                "valor": int(valor),
                "categoria": categoria
            }

            gastos.append(gasto)

            return (
                f"Gasto registrado com sucesso! ✅\n"
                f"Valor: R${valor}\n"
                f"Categoria: {categoria}"
            )
        return "Entendi! Você registrou um gasto, mas não identifiquei o valor."
    
    if text.strip() == "listar gastos":
        if not gastos:
            return "Nenhum gasto registrado ainda."
        
        resposta = "📋 Seus gastos: \n"

        total = 0

        for i, gasto in enumerate(gastos, start=1):
            resposta += f"{i}. R${gasto['valor']} - {gasto['categoria']}\n"
            total += gasto["valor"]

        resposta += f"\n💰 Total: R${total}"

        return resposta

    return f"Você enviou: {text}"