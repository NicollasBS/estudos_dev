<?php
class TesteController{
    public function handleGetRequest($id){
        if($id){
            $this->show($id);
        }else {
            $this->index();
        }
    }

    public function index(): void{
        echo 'Lista de Teste';
    }

    public function show(int $id): void{
        echo "Dados de {$id}";
    }

    public function store(): void{
        echo 'Salvando os dados';
    }

    public function update(int $id): void{
        echo "Atualizando {$id}";
    }

    public function destroy(int $id): void{
        echo "Excluindo {$id}";
    }

    
}