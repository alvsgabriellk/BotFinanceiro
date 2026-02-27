import re

def interpretar_mensagem(text):
    text = text.lower()

    comandosGastos = [
        "gastei",
        "comprei",
        "fiz uma compra",
        "paguei",
        "parcelei",
        "comprar",
        "pagar"
    ]

    if any(text.startswith(comando) for comando in comandosGastos):
        


        #valorEncontrado = re.search(r"\d+", text) procura qualquer sequencia de números"""


        #if valorEncontrado:
            #valor = valorEncontrado.group()
            #return f"Entendi!, Você registrou um gasto de R${valor:.2f}

        if text.startswith("parcelei"):
            numeros = re.findall(r"\d+", text)

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