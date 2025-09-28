<?php

use App\Core\Router;
use App\Core\Response;
require_once 'autoloader.php';
require_once 'config.php';

set_exception_handler(function ($exception) {
    Response::json(['error' => $exception->getMessage()], 500);
});

$router = new Router();

$router->adicionar('GET', '/teste', ['TesteController', 'index']);
$router->adicionar('POST', '/teste', ['TesteController', 'store']);

$router->run();
