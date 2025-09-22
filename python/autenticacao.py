import requests
import getpass
from logger import Logger

class Autenticacao:
    def __init__(self):
        self.matricula = None
        self.senha = None
        self.cpf = None
        self.url_login = 'http://172.32.1.75:8080/auth/login'
        self.url_update_password = 'http://172.32.1.75:8080/auth/users'


    def post_login(self):
        payload = {
            'matricula': self.matricula,
            'senha': self.senha
        }
        r = requests.post(self.url_login, payload)
        Logger(self.matricula, 'LOGIN')
        return r.text


    def post_update_password(self,cpf ,nova_senha, confirmacao):
        payload = {
            'matricula': self.matricula,
            'cpf': cpf,
            'senha': nova_senha,
            'confirmarSenha': confirmacao
        }
        Logger(self.matricula, 'UPDATE_PASSWORD')
        r = requests.patch(self.url_update_password, payload)
        return r.text


    def addAuth(self):
        print("É necessário informar suas credenciais para se comunicar com a API: ")
        while True:
            matricula = input("Digite sua matricula: ")
            senha = getpass.getpass("Digite sua senha: ")
            if len(matricula) == 6:
                self.matricula = matricula
                self.senha = senha
                return self.post_login()
            print("Matricula inválida! Tente novamente.")


    def updatePassword(self):
        if self.matricula is None or self.senha is None:
            print("É necessário informar suas credenciais para atualizar a senha.")
            self.addAuth()

        cpf = input("Digite seu CPF: ")
        if len(cpf) != 11:
            print("CPF inválido! Tente novamente.")
        while True:
            nova_senha = getpass.getpass("Digite sua nova senha: ")
            confirmacao = getpass.getpass("Confirme sua nova senha: ")
            if nova_senha != confirmacao:
                print("As senhas não coincidem! Tente novamente.")
                continue
            response = self.post_update_password(cpf, nova_senha, confirmacao)
            return response



if __name__ == "__main__":
    auth = Autenticacao()

    while True:
        print("\n\n[1] Autenticar")
        print("\n[2] Atualizar senha")
        print("\n[0] Sair")
        opcao = input("Digite a opção desejada: ")
        if opcao == "1":
            r = auth.addAuth()
            print(r)
        elif opcao == "2":
            r = auth.updatePassword()
            print(r)
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida! Tente novamente.")
            continue
