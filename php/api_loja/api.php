<?php

// Enviando para o client que a resposta é json
header('Content-Type: application/json; charset=utf-8');

//Filtragem dos dados da requisição
$path = explode('?', $_SERVER['REQUEST_URI'])[0];

$partes = explode('/', $path);
$partes = array_filter($partes);

$recurso = $partes[2];
$id = $partes[3];

if(!$recurso){
    http_response_code(404);
    echo json_encode(['error' => 'resource not send.']);
    exit();
}

// Encontrar o controller com base no nome do documento
$nomeController = ucfirst($recurso).'Controller';
$arquivoController = __DIR__ . "/controller/{$nomeController}.php";

// Verificar se o arquivo existe
if(!file_exists($arquivoController)){
    http_response_code(404);
    echo json_encode(['error' => 'resource not found.']);
    exit();
}

// Importa o arquivo e instancia uma nova classe, conforme o nome do controller
require_once $arquivoController;
$controller = new $nomeController();

// Salva o verbo http da requisição
$metodo = $_SERVER['REQUEST_METHOD'];

switch($metodo){
    case 'GET':
        if(!method_exists($controller, 'handleGetRequest')){
            http_response_code(405);
            echo json_encode(['error' => 'method not allowed']);
            break;
        }
        $controller->handleGetRequest($id);
        break;
    case 'POST':
        if(!method_exists($controller, 'store')){
            http_response_code(405);
            echo json_encode(['error' => 'method not allowed']);
            break;
        }
        $controller->store();
        break;
    case 'PUT':
        if(!method_exists($controller, 'update')){
            http_response_code(405);
            echo json_encode(['error' => 'method not allowed']);
            break;
        }
        $controller->update($id);
        break;
    case 'DELETE':
        if(!method_exists($controller, 'destroy')){
            http_response_code(405);
            echo json_encode(['error' => 'method not allowed']);
            break;
        }
        $controller->destroy($id);
        break;
    default:
        http_response_code(405);
        echo json_encode(['error' => 'method not allowed']);
}