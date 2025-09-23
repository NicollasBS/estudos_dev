<?php
namespace App\Controller;

class TesteController{

    public function index(): void{
        echo 'Lista de Teste';
    }

    public function show(int $id): void{
        echo "Dados de {$id}";
    }

    public function store(): void{
        $json = file_get_contents('php://input');
        $data = json_decode($json, true);
        if($data['nome'] && $data['idade']){
            $nome = $data['nome'];
            $idade = $data['idade'];
            echo json_encode(['nome' => "$nome feio", 'idade' => "$idade anos."]);
            return;
        }
        http_response_code(400);
        echo json_encode(['error'=>'Dados inválidos']);
    }

    public function update(int $id): void{
        echo "Atualizando {$id}";
    }

    public function destroy(int $id): void{
        echo "Excluindo {$id}";
    }

}
