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



meses = {
    "janeiro": "01",
    "fevereiro": "02",
    "março": "03",
    "abril": "04",
    "maio": "05",
    "junho": "06",
    "julho": "07",
    "agosto": "08",
    "setembro": "09",
    "outubro": "10",
    "novembro": "11",
    "dezembro": "12"
}        

agora = datetime.now()
mes_atual = agora.strftime("%m")
ano_atual = agora.strftime("%Y")


formaDePagamento = ["pix", "credito", "crédito", "debito", "dinheiro"]

def detectar_pagamento(text):
    text = text.lower()

    if "parcelei" in text:
        return "Credito"
    
    if "emprestimo" in text or "empréstimo" in text:
        return "Empréstimo"

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
                dataAtual = datetime.now().strftime("%Y-%m-%d %H:%M")
                dataAgora = datetime.now().strftime("%m-%d %H:%M")

                gasto = {
                    "valor": total,
                    "categoria": categoria,
                    "parcelas": parcelas,
                    "data": dataAtual,
                    "forma_pagamento": formaDePagamento,
                    "mes": mes_atual,
                    "ano": ano_atual
                }

                gastos.append(gasto)
                salvar_gastos(gastos)

                if "parcelei" in text:
                    return (
                        f"Compra parcelada registrada!✅\n"
                        f"{parcelas}x de R${valorParcela:.2f}\n"
                        f"Total: R${total:.2f}\n"
                        f"Categoria: {categoria}\n"
                        f"Data: {dataAgora}\n"
                        f"Forma de Pagamento: {formaDePagamento}"
                    )
                
                if "emprestimo" in text or "empréstimo" in text:
                    return (
                        f"Empréstimo registrado!✅\n"
                        f"{parcelas}x de R${valorParcela:.2f}\n"
                        f"Total: R${total:.2f}\n"
                        f"Categoria: {categoria}\n"
                        f"Data: {dataAgora}\n"
                        f"Forma de Pagamento: {formaDePagamento}"
                    )
            return "Entendi que é parcelamento/emprestimo, mas não identifiquei parcelas e valor corretamente"
        
        numeros = re.findall(r"\d+[.,]?\d*", text)

        if numeros:
            valores = [float(n.replace(",", ".")) for n in numeros]
            valor = max(valores)

            categoria = detectar_categoria(text)
            formaDePagamento = detectar_pagamento(text)
            dataAtual = datetime.now().strftime("%Y-%m-%d %H:%M")
            dataAgora = datetime.now().strftime("%m-%d %H:%M")
            

            gasto = {
                "valor": valor,
                "categoria": categoria,
                "data": dataAtual,
                "forma_pagamento": formaDePagamento,
                "mes": mes_atual,
                "ano": ano_atual
            }

            
            gastos.append(gasto)
            salvar_gastos(gastos)

            return (
                f"Gasto registrado com sucesso! ✅\n"
                f"Valor: R${valor:.2f}\n"
                f"Categoria: {categoria}\n"
                f"Data: {dataAgora}\n"
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

        resposta += f"\n💰 Total: R${total:.2f}"

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
    

    if text.startswith("resumo"):
        
        partes = text.split()

        # definir mes e ano
        if len(partes) == 1:
            agora = datetime.now()
            mes = agora.strftime("%m")
            ano = agora.strftime("Y")
            nomeMesExibicao = agora.strftime("%B").upper()
        else:
            nomeMesDigitado = partes[1]

            if nomeMesDigitado not in meses:
                return "Mês inválido."
            
            mes = meses[nomeMesDigitado]
            ano = datetime.now().strftime("%Y")
            nomeMesExibicao = nomeMesDigitado.upper()
        
        # filtrar mes escolhido

        gastosFiltrados = [
            g for g in gastos
            if g["mes"] == mes and g["ano"] == ano
        ]

        if not gastosFiltrados:
            return "Nenhum gasto registrado nesse mês."



        totalGeral = 0
        totalCategoria = {}
        totalPagamento = {}

        for gasto in gastosFiltrados:
            valor = gasto["valor"]
            categoria = gasto["categoria"]
            pagamento = gasto["forma_pagamento"]

            totalGeral += valor

            totalCategoria[categoria] = totalCategoria.get(categoria, 0) + valor
            totalPagamento[pagamento] = totalPagamento.get(pagamento, 0) + valor

        resposta = f"📊 RESUMO {nomeMesExibicao}\n\n"

        resposta += "💰 Total Geral: R${:.2f}\n\n".format(totalGeral)

        resposta += "📂 Por Categoria:\n"
        for cat, total in totalCategoria.items():
            resposta += f"- {cat}: R${total:.2f}\n"

        resposta += "\n💳 Por Forma de Pagamento:\n"
        for pag, total in totalPagamento.items():
            resposta += f"- {pag}: R${total:.2f}\n"

        return resposta

    return f"Você enviou: {text}"