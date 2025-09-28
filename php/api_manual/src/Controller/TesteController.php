<?php
namespace App\Controller;

use App\Core\Response;

class TesteController{
    private function getJsonData(): array{
        return (array) json_decode(file_get_contents('php://input'), true);
    }

    public function index(){
        Response::json(['message' => 'Teste :)']);
    }
    public function store(){
        Response::json(['message' => 'success', 'data' => $this->getJsonData()]);
    }
}
