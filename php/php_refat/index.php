<?php

header('Content-Type: application/json; charset=utf-8');

require_once __DIR__ . '/autoloader.php';
require_once __DIR__ . '/Router.php';
require_once __DIR__ . '/Response.php';

set_exception_handler(function($exception) {
    Response::json(['error' => $exception->getMessage()], 500);
});

$router = new Router();

$router->adicionar('GET', '/teste', ['TesteController', 'index']);
$router->adicionar('GET', '/teste/{id}', ['TesteController', 'show']);
$router->adicionar('POST', '/teste', ['TesteController', 'store']);
$router->adicionar('PUT', '/teste/{id}', ['TesteController', 'update']);
$router->adicionar('DELETE', '/teste/{id}', ['TesteController', 'destroy']);

$router->adicionar('GET', '/prod', ['TesteController', 'index']);

$router->run();
