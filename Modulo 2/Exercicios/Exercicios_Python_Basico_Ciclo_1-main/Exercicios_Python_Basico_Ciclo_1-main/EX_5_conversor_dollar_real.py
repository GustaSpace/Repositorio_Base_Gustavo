# Escreva um programa que pede ao usuário o valor atual da cotação do dollar e a quantidade de dólares para ser convertido em reais. 
# Depois mostre na tela a conversão.

# OUTPUT ESPERADO:

# Digite a cotação do dollar: 5.60
# Digite o valor em dollar a ser convetido para real: 100
# O valor em reais é:  560.0

# ------------------------------------------ ESCREVA SEU CÓDIGO ABAIXO -----------------------------------------------------------


print("Escolha uma opção: ")
print("1 - Dollar para Real")
print("2 - Real para Dollar")

opcao = int(input("Digite a opção: "))
cotacao = float(input("Informe a cotação do Dollar atual: "))

if opcao == 1:
    quant_dolar = float(input("Informe a quantidade de dólares: "))
    total_reais = quant_dolar * cotacao
    print(f"O valor em reais é R${total_reais:.2f}")
elif opcao ==2:
    quant_real = float(input("Informe a Quantidade de reais: "))
    total_dolares = quant_real / cotacao
    print(f"O valor em dólaares é ${total_dolares:.2f}")