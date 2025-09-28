<?php
namespace App\Core;

use App\Core\Response;

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
        $metodo = $_SERVER['REQUEST_METHOD'];
        $uri = explode('?', $_SERVER['REQUEST_URI'])[0];

        $uriEncontrada = false;

        foreach($this->routes as $route){
            $pattern = '#^' . preg_replace('/\{(\w+)\}/', '(\w+)', $route['path']) . '$#';

            if(preg_match($pattern, $uri, $matches)){
                $uriEncontrada = true;

                if($route['metodo'] === $metodo){
                    $handler = $route['handler'];
                    if (is_array($handler) && is_string($handler[0])) {
                        $nomeClasse = "App\\Controller\\" . $handler[0];
                        $nomeMetodo = $handler[1];
                        $controller = new $nomeClasse();

                        call_user_func_array([$controller, $nomeMetodo], $matches);
                    } else {
                        call_user_func_array($handler, $matches);
                    }
                    return;
                }
            }
        }

        if($uriEncontrada){
            Response::json(['error' => 'Method Not Allowed'], 405);
        } else {
            Response::json(['error' => 'Resource Not Found'], 404);
        }
    }
}
