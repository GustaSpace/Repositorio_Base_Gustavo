# Escreva um programa simples que pede a idade do usuário e 
# depois mostre na tela com valor BOOLEANO (True ou False) se o usuário pode tirar a CNH (Carteira Nacional de Habilitação) ou não.
# Para tirar carteira no Brasil, a idade mínima é 18 anos.

# OUTPUT ESPERADO:
# Exemplo 1:

# Digite sua idade: 19
# Pode tirar carteira de motorista? True

# Exemplo 2:
# Digite sua idade: 17
# Pode tirar carteira de motorista? False

# ------------------------------------------ ESCREVA SEU CÓDIGO ABAIXO -----------------------------------------------------------

idade = int(input("Qual sua idade? "))
possui_carteira = input("Possui carteira de motorista? \n (1-Sim / 2-Não) ")

if idade >= 18 and possui_carteira == "1":
  print('Pode dirigir')
elif possui_carteira == "2":
  print('Não pode dirigir')
elif idade < 18:
  print('Menor de idade')

#-------------------------------------------------------------

nome = input("Qual é o seu nome? ")
idade = int(input("Qual sua idade? "))
possui_carteira = input("Possui carteira de motorista? \n (1-Sim / 2-Não) ")

if idade >= 18:
    if possui_carteira == "1":
        print("Pode dirigir")
    else:
        print("Não pode dirigir")
else:
    print("Menor de idade")