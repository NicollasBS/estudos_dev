import requests
from getpass import getpass
import re
from rep import Repositorio
import sqlite3
from config import Config

class Autenticacao:
    def __init__(self, repositorio: Repositorio):
        self.repositorio = repositorio
        self.config = Config()
        self.matricula = ''
        self.senha = ''
        self.cpf = ''
        self.nome = ''
        self.url_login = self.config.AUTH_LOGIN_URL
        self.url_users = self.config.AUTH_USERS_URL
        self.config = Config()

    def login(self, matricula_entrada, senha_entrada):
        if not self._matricula_validacao(matricula_entrada):
            return
        self.matricula = matricula_entrada
        self.senha = senha_entrada
        payload = {"matricula":self.matricula, "senha": self.senha}
        try:
            r = requests.post(self.url_login, json=payload)
            r.raise_for_status()
            json_resonse = r.json()
            matricula = json_resonse['usuario']['matricula']
            token = json_resonse['token_access']
            sql = "INSERT INTO login(matricula, token) VALUES(?, ?)"
            resultado = self.repositorio.executar(sql, (matricula, token))
            if resultado is not None:
                print("\nLogin bem-sucedido! Token salvo no banco de dados local.")
            else:
                print("\nLogin bem-sucedido, mas falha ao salvar o token localmente.")
        except requests.exceptions.RequestException as e:
            print(f"\nFalha na comunicação com o servidor: {e}")
        except Exception as e:
            print(f"\nOcorreu um erro inesperado: {e}") 

    def atualizar_senha(self, matricula_entrada, cpf_entrada, nome_entrada, senha_entrada, confirmacao_senha):
        if not self._matricula_validacao(matricula_entrada):
            return
        if not self._cpf_validacao(cpf_entrada):
            return
        if(senha_entrada != confirmacao_senha):
            print("As senhas não coincidem.")
            return
        self.matricula = matricula_entrada
        self.cpf = cpf_entrada
        self.nome = nome_entrada
        self.senha = senha_entrada
        
        payload = {
            "matricula": self.matricula,
            "cpf": self.cpf,
            "nome": self.nome,
            "senha": self.senha,
            "confirmacaoSenha": self.senha
        }
        r = requests.patch(self.url_users, json=payload)
        if r.status_code == 200:
            print("Senha atualizada com sucesso!")
            return
        else:
            print("Houve algum erro ao tentar atualizar a senha.")

    def _matricula_validacao(self, matricula_entrada):
        if re.fullmatch(r"^\d{6}$", matricula_entrada):
            return True
        else:
            print('Matricula inválida')
            return False

    def _cpf_validacao(self, cpf_entrada):
        if re.fullmatch(r"^\d{11}$", cpf_entrada):
            return True
        else:
            print('CPF inválido')
            return False
        pass

