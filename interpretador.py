import re # encontra padrões / extrai dados / valida formatos

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
                    f"Compra parcelada detectada!\n"
                    f"{parcelas}x de R${valorParcela}\n"
                    f"Total: R${total}"
                )
            return "Entendi que é parcelado, mas não identifiquei parcelas e valor corretamente"
        
        numeros = re.findall(r"\d+", text)

        if numeros:
            valor = max(numeros, key=int)
            return f"Entendi!, você registrou um gasto de R${valor}"
        
        return "Entendi! Você registrou um gasto, mas não identifiquei o valor."

    return f"Você enviou: {text}"