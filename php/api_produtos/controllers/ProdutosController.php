<?php

require_once __DIR__ . '/../db/Database.php';

class ProdutosController{

    private PDO $pdo;

    public function __construct(){
        $this->pdo = Database::getInstance();
    }

    //Se vier um ID no GET, método show, se não, método index
    public function handleGetRequest(int $id = null): void{
        if($id){
            $this->show($id);
        }else {
            $this->index();
        }
    }

    public function index(): void{
        $stmt = $this->pdo->query("SELECT id, nome, preco FROM produtos");
        $produtos = $stmt->fetchAll(PDO::FETCH_ASSOC);
        echo json_encode($produtos);
    }

    public function show(int $id): void{
        $stmt = $this->pdo->prepare("SELECT id, nome, preco FROM produtos where id = ?");
        $stmt->execute([$id]);
        $produto = $stmt->fetchAll(PDO::FETCH_ASSOC);
        if($produto){
            echo json_encode($produto);
        }else{
            http_response_code(404);
            echo json_encode(['erro' => 'Produto não encontrado']);
        }
    }

    public function store(): void{
        $corpo = file_get_contents('php://input');
        $dados = json_decode($corpo, true);

        if(!isset($dados['nome']) && !isset($dados['preco'])){
            http_response_code(400);
            $resposta = ['error' => "Dados incompletos."];
            return;
        }

        try{
            $stmt = $this->pdo->prepare("INSERT INTO produtos(nome, preco) values(?,?)");
            $stmt->execute([$dados['nome'], $dados['preco']]);
            $idCriado = $this->pdo->lastInsertId();

            http_response_code(201);
            echo json_encode([
            'message'=>'success',
            'id'=>$idCriado,
            'data'=>$dados
            ]);
        }catch (PDOException $e){
            http_response_code(500);
            echo json_encode(['erro'=>"Erro ao salvar produto: ".$e->getMessage()]);
        }
    }

    public function update(int $id): void{
        $corpo = file_get_contents('php://input');
        $dados = json_decode($corpo, true);

        if(empty($dados)){
            http_response_code(400);
            echo json_encode(['error' => 'Nenhum dado enviado para atualização ou JSON inválido']);
            return;
        }

        $setClauses = [];
        $params = [];

        if(isset($dados['nome'])){
            $setClauses[] = "nome = ?";
            $params[] = $dados['nome'];
        }

        if(isset($dados['preco'])){
            $setClauses[] = "preco = ?";
            $params[] = $dados['preco'];
        }

        if(empty($setClauses)){
            http_response_code(400);
            echo json_encode(['erro' => 'Nenhum campo enviado para atualização.']);
            return;
        }

        $params[] = $id;

        $setString = implode(', ', $setClauses);

        $sql = "UPDATE produtos SET {$setString} WHERE id = ?";

        try{
            $stmt = $this->pdo->prepare($sql);
            $stmt->execute($params);

            if($stmt->rowCount()===0){
                http_response_code(404);
                echo json_encode(['error' => 'Nenhum produto encontrado com este ID para atualizar.']);
                return;
            }else {
                echo json_encode(['message' => 'Produto atualizado com sucesso']);
                return;
            }
        } catch (PDOException $e){
            http_response_code(500);
            echo json_encode(['erro' => 'Erro ao atualizar dados: ' . $e->getMessage()]);
            return;
        }

    }

    public function destroy(int $id): void{
        try{
            $stmt = $this->pdo->prepare("DELETE FROM produtos WHERE id = ?");
            $stmt->execute([$id]);
            if($stmt->rowCount() === 0){
                http_response_code(404);
                echo json_encode(['error'=>'Nenhum produto com este ID para deletar']);
                return;
            }else{
                http_response_code(204);
            }
        }catch (PDOException $e){
            echo json_encode(['error' => 'Erro ao deletar item: ' . $e->getMessage()]);
        }



    }

}

?>
