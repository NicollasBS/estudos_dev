<?php
class Router{
    private $routes = [];

    public function adicionar(string $metodo, string $path, callable|array $handler): void{
        $this->routes[] = [
            'metodo' => $metodo,
            'path' => $path,
            'handler' => $handler
        ];
    }

    public function run(): void{
        $metodoRequisicao = $_SERVER['REQUEST_METHOD'];
        $uriRequisicao = explode('?', $_SERVER['REQUEST_URI'])[0];

        $uriEncontrada = false;

        foreach($this->routes as $route){
            $pattern = '#^' . preg_replace('/\{(\w+)\}/', '(\w+)', $route['path']) . '$#';

            if (preg_match($pattern, $uriRequisicao, $matches)){
                
                $uriEncontrada = true;

                if ($route['metodo'] === $metodoRequisicao) {
                    
                    array_shift($matches);
                    $handler = $route['handler'];
                    if (is_array($handler) && is_string($handler[0])) {
                        $className = "App\\Controller\\" . $handler[0];
                        $methodName = $handler[1];
                        
                        $controller = new $className();
                        
                        call_user_func_array([$controller, $methodName], $matches);
                    } else {
                        call_user_func_array($handler, $matches);
                    }
                    return;
                }
            }
        }

        if ($uriEncontrada) {
            http_response_code(405);
            echo json_encode(['error' => 'Method Not Allowed']);
        } else {
            http_response_code(404);
            echo json_encode(['error' => 'Resource Not Found']);
        }
    }
}
