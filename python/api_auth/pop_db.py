# populate_db.py
import os
from database_repository import DatabaseRepository

# --- CONFIGURAÇÕES ---
DB_FILE = 'auth_system.db'
NUM_USERS_TO_CREATE = 10000
CREDENTIALS_FILE = 'login_credentials.csv' # Arquivo para salvar os logins para o Locust usar

def populate():
    # Apaga o banco de dados antigo para começar do zero
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"Banco de dados '{DB_FILE}' antigo removido.")

    repo = DatabaseRepository(db_name=DB_FILE)
    print("Iniciando a criação de usuários...")

    # Usamos um arquivo para salvar os dados para o Locust ler depois
    with open(CREDENTIALS_FILE, 'w') as f:
        f.write("username,password\n") # Header do CSV

        for i in range(NUM_USERS_TO_CREATE):
            username = f"user{i}"
            password = f"password{i}"

            user_id = repo.create_user(username, password)

            if user_id:
                f.write(f"{username},{password}\n")
                if (i + 1) % 500 == 0:
                    print(f"   {i + 1}/{NUM_USERS_TO_CREATE} usuários criados...")
            else:
                print(f"Erro ao criar o usuário {username}")

    print("-" * 30)
    print(f"SUCESSO: {NUM_USERS_TO_CREATE} usuários criados.")
    print(f"Credenciais salvas em '{CREDENTIALS_FILE}' para o teste de carga.")

if __name__ == '__main__':
    populate()
