# locustfile_login.py
import random
from locust import HttpUser, task, between

class LoginUser(HttpUser):
    wait_time = between(0.5, 2.5) # Espera entre 0.5 e 2.5 segundos
    host = "http://localhost:8001"

    # Esta lista irá armazenar todos os usuários que criamos
    credentials = []

    def on_start(self):
        """
        Isso é executado uma vez por usuário virtual quando ele é iniciado.
        Carregamos as credenciais do arquivo para a memória.
        """
        if not LoginUser.credentials:
            print("Carregando credenciais do arquivo...")
            with open('login_credentials.csv', 'r') as f:
                # Pula o header
                next(f)
                for line in f:
                    username, password = line.strip().split(',')
                    LoginUser.credentials.append({"username": username, "password": password})
            print(f"{len(LoginUser.credentials)} credenciais carregadas.")

    @task
    def mass_login(self):
        """
        Pega um usuário aleatório da lista e tenta fazer o login.
        Isso testa o "caminho feliz" do login.
        """
        if not LoginUser.credentials:
            print("Nenhuma credencial para testar.")
            return

        # Escolhe um usuário aleatório da nossa lista
        random_user = random.choice(LoginUser.credentials)

        # Usamos um 'catch_response' para verificar se o status code é 200 (OK)
        with self.client.post("/login", json=random_user, catch_response=True, name="/login (success)") as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(
                    f"Falha no login do usuário {random_user['username']}. "
                    f"Status: {response.status_code}, Resposta: {response.text}"
                )
