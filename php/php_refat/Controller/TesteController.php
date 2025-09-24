<?php
namespace App\Controller;

use Response;

require_once __DIR__ . '/../Response.php';

class TesteController{

    public function index(): void{
        Response::json(['message' => 'Lista de Teste']);
    }

    public function show(int $id): void{
        Response::json(['data' => "Dados de {$id}"]);
    }

    public function store(): void{
        $json = file_get_contents('php://input');
        $data = json_decode($json, true);
        if($data['nome'] && $data['idade']){
            $nome = $data['nome'];
            $idade = $data['idade'];
            Response::json(['nome' => "$nome feio", 'idade' => "$idade anos."], 201);
            return;
        }
        Response::json(['error'=>'Dados inválidos'], 400);
    }

    public function update(int $id): void{
        Response::json(['message' => "Atualizando {$id}"]);
    }

    public function destroy(int $id): void{
        Response::json(['message' => "Deletando {$id}"], 204);
    }
}
