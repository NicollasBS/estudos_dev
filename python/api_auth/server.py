import http.server
import socketserver
import json
import threading
from queue import Queue

from database_repository import DatabaseRepository
from auth_worker import AuthWorker
from crud_worker import CrudWorker

# CONFIGURAÇÕES SERVIDOR
HOST = 'localhost'
PORT = 8001
AUTH_ROUTES = ['/login']
CRUD_ROUTES = ['/user/update', '/user/delete', '/register']

# INICIALIZAÇÃO DE FILAS E REPOSITÓRIOS
auth_queue = Queue()
crud_queue = Queue()
db_repo = DatabaseRepository()

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        request_finished_event = threading.Event()

        body={}
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            body = json.loads(post_data)
        except (TypeError, ValueError, json.JSONDecodeError):
            self.send_error(400, 'Bad Request: JSON inválido')
            return

        path = self.path

        if path in AUTH_ROUTES:
            task = (self, path, body, request_finished_event)
            auth_queue.put(task)
        elif path in CRUD_ROUTES:
            task = (self, path, self.headers, body, request_finished_event)
            crud_queue.put(task)
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Endpoint não encontrado'}).encode('utf-8'))
            return

        request_finished_event.wait()

def run_server():
    auth_worker = AuthWorker(auth_queue, db_repo)
    auth_worker.start()

    crud_worker = CrudWorker(crud_queue, db_repo)
    crud_worker.start()

    class ThreadingTCPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
        pass

    with ThreadingTCPServer((HOST, PORT), RequestHandler) as httpd:
        print(f"Gateway servindo em http://{HOST}:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor desligando...")
            httpd.shutdown()

if __name__ == '__main__':
    run_server()
