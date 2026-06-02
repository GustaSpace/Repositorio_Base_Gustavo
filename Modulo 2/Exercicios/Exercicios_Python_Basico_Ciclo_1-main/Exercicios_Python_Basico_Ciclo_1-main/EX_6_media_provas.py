# Escreva um programa que pede ao usuário o nome de um aluno e as notas de 3 provas que este aluno realizou.
# No fim o programa deve mostrar na tela a média das 3 provas
# Dica:
# Para calcular a média das provas você deve dividir a soma das notas das provas pela quantidade de provas realizadas
# media = soma / 3

# OUTPUT ESPERADO:

# | ______________________________ |
# | SISTEMA DE PROVAS
# | ______________________________ |
# | Nome do aluno: Fulano
# | Nota da primeira prova: 9.8
# | Nota da segunda prova: 7
# | Nota da terceira prova: 8.5
# | ______________________________ |
# | Aluno: Fulano 
# | Média: 8.43
# | Aluno aprovado
# | ______________________________ |

# ------------------------------------------ ESCREVA SEU CÓDIGO ABAIXO -----------------------------------------------------------



#nome = input("Nome do aluno: ")
#nota1 = float(input("Nota da prova global: "))
#nota2 = float(input("Nota da prova simulado: "))
#nota3 = float(input("Nota da prova trabalho: "))

#media = (nota1 + nota2 + nota3) / 3


#print(f"Aluno: {nome}")
#print(f"média: {media:.2f}")
#print("Aluno Aprovado")

from colorama import Fore, Style
print('\n_-_-_-_ Calculadora de Média _-_-_-_\n')
aluno = input('Nome do Aluno: ')

p1 = float(input("| NOta da primeira prova: "))
p2 = float(input("| NOta da segunda prova: "))
p3 = float(input("| NOta da terceira prova: "))

media = (p1 + p2 + p3) / 3

print(f"| Aluno: {aluno}")
print(f"| Média: {media:.2f}")

if media >= 6:
    print(Fore.GREEN+"| Aluno aprovado", Style.RESET_ALL)
else:
    print(Fore.RED+"| Aluno aprovado", Style.RESET_ALL)