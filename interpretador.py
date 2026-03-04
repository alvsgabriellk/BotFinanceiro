import re # encontra padrões / extrai dados / valida formatos
import os
import json
from datetime import datetime

CAMINHO_ARQUIVO = "data/gastos.json"


def carregar_gastos():
    if not os.path.exists(CAMINHO_ARQUIVO):
        return []

    if os.path.getsize(CAMINHO_ARQUIVO) == 0:
        return []
    
    with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)


    
    

def salvar_gastos(gastos):
    with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(gastos, f, indent=4, ensure_ascii=False)


formaDePagamento = ["pix", "credito", "crédito", "debito", "dinheiro"]

def detectar_pagamento(text):
    for pagamento in formaDePagamento:
        if pagamento in text:
            return pagamento.capitalize()
    return "Não Informado"


gastos = carregar_gastos()

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
        "emprestimo",

        "eu paguei",
        "eu comprei",
        "eu fiz uma compra",
        "fiz uma compra",
        "eu gastei",
        "eu parcelei",
        "eu fiz um emprestimo",
        "eu fiz um empréstimo",
        "fiz um emprestimo",
        "eu fiz um empréstimo"
    ]
       #retorn true se apns um for tru        # percorre a lista toda
    if any(text.startswith(comando) for comando in comandosGastos):
        #text.starswith - verifica se começa com o comando


        #re.search(r"\d+", text) procura qualquer sequencia de números"""


        if "parcelei" in text or "emprestimo" in text or "empréstimo" in text:
            numeros = re.findall(r"\d+[.,]?\d*", text) # encontre todas sequencias de numeros no texto / + um ou mais

            if len(numeros) >= 2:

                valores = [float(n.replace(",", ".")) for n in numeros]

                parcelas = int(min(valores))
                valorParcela = max(valores)
                categoria = detectar_categoria(text)

                total = (parcelas) * (valorParcela)

                formaDePagamento = detectar_pagamento(text)
                data_atual = datetime.now().strftime("%Y-%m-%d %H:%M")

                gasto = {
                    "valor": total,
                    "categoria": categoria,
                    "parcelas": parcelas,
                    "data": data_atual,
                    "forma_pagamento": formaDePagamento
                }

                gastos.append(gasto)
                salvar_gastos(gastos)

                if "parcelei" in text:
                    return (
                        f"Compra parcelada registrada!✅\n"
                        f"{parcelas}x de R${valorParcela:.2f}\n"
                        f"Total: R${total:.2f}\n"
                        f"Categoria: {categoria}"
                        f"Data: {data_atual}"
                        f"Forma de Pagamento: {formaDePagamento}"
                    )
                
                if "emprestimo" in text or "empréstimo" in text:
                    return (
                        f"Empréstimo registrado!✅\n"
                        f"{parcelas}x de R${valorParcela:.2f}\n"
                        f"Total: R${total:.2f}\n"
                        f"Categoria: {categoria}"
                        f"Data: {data_atual}"
                        f"Forma de Pagamento: {formaDePagamento}"
                    )
            return "Entendi que é parcelamento/emprestimo, mas não identifiquei parcelas e valor corretamente"
        
        numeros = re.findall(r"\d+[.,]?\d*", text)

        if numeros:
            valores = [float(n.replace(",", ".")) for n in numeros]
            valor = max(valores)

            categoria = detectar_categoria(text)
            formaDePagamento = detectar_pagamento(text)
            data_atual = datetime.now().strftime("%Y-%m-%d %H:%M")
            

            gasto = {
                "valor": valor,
                "categoria": categoria,
                "data": data_atual,
                "forma_pagamento": formaDePagamento
            }

            
            gastos.append(gasto)
            salvar_gastos(gastos)

            return (
                f"Gasto registrado com sucesso! ✅\n"
                f"Valor: R${valor:.2f}\n"
                f"Categoria: {categoria}"
                f"Data: {data_atual}"
                f"Forma de pagamento: {formaDePagamento}"
            )
        return "Entendi! Você registrou um gasto, mas não identifiquei o valor."
    
    if text.strip() == "listar gastos":
        if not gastos:
            return "Nenhum gasto registrado ainda."
        
        resposta = "📋 Seus gastos: \n"

        total = 0

        for i, gasto in enumerate(gastos, start=1):
            resposta += f"{i}. R${gasto['valor']:.2f} - {gasto['categoria']}\n"
            total += gasto["valor"]

        resposta += f"\n💰 Total: R${total}"

        return resposta
    
    if text.startswith("remover"):
        numeros = re.findall(r"\d+", text)

        if not numeros:
            return "Informe o número do gasto que deseja remover."
        
        indice = int(numeros[0]) - 1

        if 0 <= indice < len(gastos):
            removido = gastos.pop(indice)
            salvar_gastos(gastos)

            return (
                f"Gasto removido! 🗑\n"
                f"Valor: R${removido['valor']:.2f}\n"
                f"Categoria: {removido['categoria']}"
            )
        return "Número inválido."

    return f"Você enviou: {text}"