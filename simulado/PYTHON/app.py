from auth import Autenticacao
from rep import Repositorio
from config import Config
from getpass import getpass

def menu():
    print("__________________________________")
    print("Escolha sua opção")
    print("[1] Salvar Token de Acesso")
    print("[2] Atualizar senha")
    print("[0] Sair")


if __name__ == '__main__':
    config = Config()
    rep = Repositorio(config.DATABASE_NAME)
    auth = Autenticacao(rep)

    print("Garantindo que a tabela 'login' exista...")
    rep.executar("""
        CREATE TABLE IF NOT EXISTS login (
            matricula TEXT,
            token TEXT NOT NULL
        )
    """)
    print("Tabela verificada com sucesso.")

    while True:

        menu()
        escolha = input('Digite sua opção: ')
        match escolha:
            case '1':
                matricula = input('Digite sua matricula: ')
                senha = getpass('Digite sua senha: ')
                auth.login(matricula, senha)
                continue
            case '2':
                matricula = input("Digite sua matricula: ")
                cpf = input("Digite seu CPF(apenas dígitos): ")
                nome = input("Digite seu nome: ")
                senha = getpass("Digite sua nova senha: ")
                confirmacao_senha = getpass("Confirme a sua  nova senha: ")
                auth.atualizar_senha(matricula, cpf, nome, senha, confirmacao_senha)
                continue
            case '0':
                rep.fechar()
                exit()
            case _:
                print('Opção inválida')
                continue


    