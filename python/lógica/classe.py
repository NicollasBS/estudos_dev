class Animal:
    def __init__(self, nome, especie, qtd_patas) -> None:
        self.nome = nome
        self.especie = especie
        self.qtd_patas = qtd_patas

    def andar(self):
        print("Andando...")

    def comer(self):
        print("Comendo...")

    def __str__(self):
        return f"Nome: {self.nome}, Espécie: {self.especie}, Patas: {self.qtd_patas}"

if __name__ == "__main__":
    animal = Animal("Leão", "Felino", 4)
    print(animal)
    animal.andar()
    animal.comer()
