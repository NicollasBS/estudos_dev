<?php

header('Content-Type: application/json; charset=utf-8');

$path = explode('?', $_SERVER['REQUEST_URI'])[0];

$parts = explode('/', $path);
$parts = array_filter($parts);

$recurso = $parts[2] ?? null;
$id = $parts[3] ?? null;

if (!$recurso) {
    http_response_code(404);
    echo json_encode(['erro' => 'Recurso deve ser enviado']);
    exit;
}

$controllerName = ucfirst($recurso) . 'Controller';
$controllerFile = __DIR__ . "/controllers/{$controllerName}.php";

if (!file_exists($controllerFile)) {
    http_response_code(404);
    echo json_encode(['erro' => "O recurso '$recurso' não existe."]);
    exit;
}

require_once $controllerFile;
$controller = new $controllerName();

$metodo = $_SERVER['REQUEST_METHOD'];

switch ($metodo) {
    case 'GET':
        $controller->handleGetRequest($id);
        break;
    case 'POST':
        $controller->store();
        break;
    case 'PUT':
        $controller->update($id);
        break;
    case 'DELETE':
        $controller->destroy($id);
        break;
    default:
        http_response_code(405);
        echo json_encode(['erro' => 'Método não permitido']);
        break;
}

?>
