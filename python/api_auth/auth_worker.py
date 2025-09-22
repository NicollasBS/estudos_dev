# auth_worker.py
import threading
import json

class AuthWorker(threading.Thread):
    def __init__(self, task_queue, repository):
        super().__init__()
        self.task_queue = task_queue
        self.repository = repository
        self.daemon = True

    def run(self):
        print("Auth Worker iniciado (apenas para login)...")
        while True:
            request_handler, path, body, event = self.task_queue.get()
            try:
                if path == '/login':
                    self.handle_login(request_handler, body)
                else:
                    self.send_response(request_handler, 404, {'error': 'Endpoint não encontrado no Auth Worker'})
            except Exception as e:
                print(f"Erro inesperado no processamento do Auth Worker: {e}")
            finally:
                self.task_queue.task_done()
                event.set()

    # --- FUNÇÃO MODIFICADA ---
    def send_response(self, handler, status_code, body):
        try:
            handler.send_response(status_code)
            handler.send_header('Content-type', 'application/json')
            handler.end_headers()
            handler.wfile.write(json.dumps(body).encode('utf-8'))
        except (BrokenPipeError, ConnectionResetError) as e:
            print(f"AVISO: O cliente desconectou antes da resposta ser enviada. Erro: {e}")

    def handle_login(self, handler, body):
        username = body.get('username')
        password = body.get('password')

        if not username or not password:
            self.send_response(handler, 400, {'error': 'Usuário e senha são obrigatórios'})
            return

        user = self.repository.check_password(username, password)
        if user:
            token = self.repository.create_session(user['id'])
            self.send_response(handler, 200, {'message': 'Login bem-sucedido', 'token': token})
        else:
            self.send_response(handler, 401, {'error': 'Credenciais inválidas'})
