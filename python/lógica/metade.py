from math import ceil
entrada = input("Digite um número: ")
try:
    numero = int(entrada)
except:
    print("Entrada inválida")
    exit()

metade = ceil(numero / 2)
for i in range(numero):
    print(i)
    if(i == metade):
        print(f"Estamos na metade já meu chegado {i}")

print(f"Terminou... Chegamos no {numero} Obrigado!")

lista = ['p1', 'pw', 'asd']
for item in lista:
    print(item)
