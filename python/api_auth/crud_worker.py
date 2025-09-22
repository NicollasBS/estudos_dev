# crud_worker.py
import threading
import json

class CrudWorker(threading.Thread):
    def __init__(self, task_queue, repository):
        super().__init__()
        self.task_queue = task_queue
        self.repository = repository
        self.daemon = True

    def run(self):
        print("CRUD Worker iniciado (para registro, update e delete)...")
        while True:
            request_handler, path, headers, body, event = self.task_queue.get()
            try:
                if path == '/register':
                    self.handle_register(request_handler, body)
                else:
                    user = self.authenticate(headers)
                    if not user:
                        self.send_response(request_handler, 401, {'error': 'Token de autorização inválido ou ausente'})
                    elif path == '/user/update' and request_handler.command == 'POST':
                        self.handle_update(request_handler, user, body)
                    elif path == '/user/delete' and request_handler.command == 'POST':
                        self.handle_delete(request_handler, user)
                    else:
                        self.send_response(request_handler, 404, {'error': 'Endpoint protegido não encontrado no CRUD Worker'})
            except Exception as e:
                # O erro principal será capturado pelo send_response,
                # mas mantemos este bloco para outros erros inesperados.
                print(f"Erro inesperado no processamento do CRUD Worker: {e}")
            finally:
                self.task_queue.task_done()
                event.set()

    def authenticate(self, headers):
        auth_header = headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        token = auth_header.split(' ')[1]
        return self.repository.get_user_by_token(token)

    # --- FUNÇÃO MODIFICADA ---
    def send_response(self, handler, status_code, body):
        """
        Envia a resposta de forma segura, tratando erros de conexão
        caso o cliente já tenha desconectado.
        """
        try:
            handler.send_response(status_code)
            handler.send_header('Content-type', 'application/json')
            handler.end_headers()
            handler.wfile.write(json.dumps(body).encode('utf-8'))
        except (BrokenPipeError, ConnectionResetError) as e:
            # Esta é a parte importante!
            # Apenas registramos um aviso e seguimos em frente. A thread não quebra.
            print(f"AVISO: O cliente desconectou antes da resposta ser enviada. Erro: {e}")

    # O resto das funções (handle_register, handle_update, handle_delete) permanecem as mesmas...
    def handle_register(self, handler, body):
        username = body.get('username')
        password = body.get('password')

        if not username or not password:
            self.send_response(handler, 400, {'error': 'Usuário e senha são obrigatórios'})
            return

        user_id = self.repository.create_user(username, password)
        if user_id:
            self.send_response(handler, 201, {'message': 'Usuário criado com sucesso', 'user_id': user_id})
        else:
            self.send_response(handler, 409, {'error': 'Usuário já existe'})

    def handle_update(self, handler, user, body):
        new_username = body.get('new_username')
        if not new_username:
            self.send_response(handler, 400, {'error': 'O campo "new_username" é obrigatório'})
            return

        success = self.repository.update_username(user['id'], new_username)
        if success:
            self.send_response(handler, 200, {'message': f'Usuário atualizado para {new_username}'})
        else:
            self.send_response(handler, 409, {'error': 'Novo nome de usuário já está em uso'})

    def handle_delete(self, handler, user):
        success = self.repository.delete_user(user['id'])
        if success:
            self.send_response(handler, 200, {'message': f'Usuário {user["username"]} deletado com sucesso'})
        else:
            self.send_response(handler, 500, {'error': 'Não foi possível deletar o usuário'})
