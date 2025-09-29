<?php

use App\Core\Response;
use App\Core\Router;

require_once __DIR__ . '/autoloader.php';
require_once __DIR__ . '/config.php';

set_exception_handler(function($exception) {
    Response::json(['error' => $exception->getMessage()], 500);
});

$router = new Router();

$router->adicionar('GET', '/user', ['UserController', 'index']);
$router->adicionar('GET', '/user/{id}', ['UserController', 'show']);
$router->adicionar('POST', '/user', ['UserController', 'store']);
$router->adicionar('PUT', '/user/{id}', ['UserController', 'update']);
$router->adicionar('DELETE', '/user/{id}', ['UserController', 'destroy']);

$router->run();