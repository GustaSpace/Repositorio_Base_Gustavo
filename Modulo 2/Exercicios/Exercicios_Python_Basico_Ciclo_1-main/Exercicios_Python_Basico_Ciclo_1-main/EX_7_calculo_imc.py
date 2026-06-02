# Escreva um código que pede ao usuário a altura e o peso e faça o cálculo do IMC (Índice de massa corporal) do usuário.
# Dica:
# Para calcular o IMC você deve dividir o peso pela altura ao quadrado
# imc = peso / (altura ** 2)


# OUTPUT ESPERADO:

# Digite sua altura: 1.78
# Digite seu peso: 85
# O seu IMC é: 26.83

# ------------------------------------------ ESCREVA SEU CÓDIGO ABAIXO -----------------------------------------------------------


print('\nCalculadora de IMC\n')
nome = input('Digite seu nome: ')
altura = float(input('Digite sua altura(ex 1.70): '))
peso = float(input('Digite seu peso(ex 70): '))

# fórmula imc = peso / (altura ** 2)

imc = peso / (altura ** 2) # * multiplica, ** potência
imc = round(imc,2) # round está arredondando o imc para 2 casas decimais

print(f'''
        Resultado:
                    PACIENTE: {nome}
                    PESO: {peso}
                    ALTURA: {altura}
                 ______________________
                |                      |       
                |    IMC = {imc}       |   
                |______________________|      
            Obrigado por usar nosso app
            
''')