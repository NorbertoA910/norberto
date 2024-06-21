import random

secreto = random.randint(0,9)

dificuldade = input("Escolhe uma dificuldade(f = facil; m = medio, d = dificil)")

if dificuldade == "f":
    vidas = 10

if dificuldade == "m":
    vidas = 5

if dificuldade == "d":
    vidas = 2

if dificuldade == "i":
    vidas = 1

while True:
    user = int(input("Adivinha uma numero de 0, 9: "))
    print(user)

    if secreto < user:
        vidas = vidas - 1
        print("O numero é menor do que " + str(user))

    if secreto > user:
        vidas = vidas - 1
        print("O numero é maior do que " + str(user))

    if secreto == user:
        print("Adivinhaste! Tinhas mais " + str(vidas) + " vidas.")
        dificuldade = input("Escolhe uma dificuldade(f = facil; m = medio, d = dificil)")

    if vidas == 0:
        print("Perdeste. O numero era " + str(secreto))
        dificuldade = input("Escolhe uma dificuldade(f = facil; m = medio, d = dificil)")

    