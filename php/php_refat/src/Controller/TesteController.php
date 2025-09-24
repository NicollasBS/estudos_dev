<?php
namespace App\Controller;

use Response;

require_once __DIR__ . '/../Core/Response.php';

class TesteController{

    public function index(): void{
        Response::json(['message' => 'Lista de Teste']);
    }

    public function show(int $id): void{
        Response::json(['data' => "Dados de {$id}"]);
    }

    public function store(): void{
        Response::json(['message'=>'Dados atualizados']);
    }

    public function update(int $id): void{
        Response::json(['message' => "Atualizando {$id}"]);
    }

    public function destroy(int $id): void{
        Response::json(null, 204);
    }
}
