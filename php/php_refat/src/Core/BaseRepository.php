<?php
namespace App\Core;

use App\Core\Database;
use PDO;

class BaseRepository {
    protected PDO $pdo;
    protected string $tabela;

    public function __construct(){
        $this->pdo = Database::getInstance();
    }

    public function findAll(): array{
        $pdo = Database::getInstance();
        $stmt = $pdo->query("SELECT * FROM {$this->tabela}");
        return $stmt->fetchAll();
    }

    public function find(int $id): mixed{
        $pdo = Database::getInstance();
        $stmt = $pdo->prepare("SELECT * FROM {$this->tabela} WHERE id = :id");
        $stmt->execute(['id' => $id]);
        return $stmt->fetch();
    }

    public function insert(array $dados): string{
        $pdo = Database::getInstance();
        $colunas = implode(', ', array_keys($dados));
        $placeholders = ":" . implode(', :', array_keys($dados));

        $sql = "INSERT INTO {$this->tabela} ($colunas) VALUES ($placeholders)";

        $stmt = $pdo->prepare($sql);
        $stmt->execute($dados);

        return $pdo->lastInsertId();
    }

    public function update(int $id, array $dados): bool {
            $pdo = Database::getInstance();

            $set = [];
            foreach ($dados as $coluna => $valor) {
                $set[] = "{$coluna} = :{$coluna}";
            }
            $setSql = implode(', ', $set);

            $sql = "UPDATE {$this->tabela} SET {$setSql} WHERE id = :id";

            $dados['id'] = $id;

            $stmt = $pdo->prepare($sql);
            return $stmt->execute($dados);
        }

    public function delete(int $id): bool {
            $pdo = Database::getInstance();
            $stmt = $pdo->prepare("DELETE FROM {$this->tabela} WHERE id = :id");
            return $stmt->execute(['id' => $id]);
        }
}
