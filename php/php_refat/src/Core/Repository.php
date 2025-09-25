<?php
namespace App\Core;

use App\Core\Database;

class Repository {
    public static function findAll(string $tabela): array{
        $pdo = Database::getInstance();
        $stmt = $pdo->query("SELECT * FROM {$tabela}");
        return $stmt->fetchAll();
    }

    public static function find(string $tabela, int $id): mixed{
        $pdo = Database::getInstance();
        $stmt = $pdo->prepare("SELECT * FROM {$tabela} WHERE id = :id");
        $stmt->execute(['id' => $id]);
        return $stmt->fetch();
    }

    public static function insert(string $tabela, array $dados): string{
        $pdo = Database::getInstance();
        $colunas = implode(', ', array_keys($dados));
        $placeholders = ":" . implode(', :', array_keys($dados));

        $sql = "INSERT INTO {$tabela} ($colunas) VALUES ($placeholders)";

        $stmt = $pdo->prepare($sql);
        $stmt->execute($dados);

        return $pdo->lastInsertId();
    }

    public static function update(string $tabela, int $id, array $dados): bool {
            $pdo = Database::getInstance();

            $set = [];
            foreach ($dados as $coluna => $valor) {
                $set[] = "{$coluna} = :{$coluna}";
            }
            $setSql = implode(', ', $set);

            $sql = "UPDATE {$tabela} SET {$setSql} WHERE id = :id";

            $dados['id'] = $id;

            $stmt = $pdo->prepare($sql);
            return $stmt->execute($dados);
        }

    public static function delete(string $tabela, int $id): bool {
            $pdo = Database::getInstance();
            $stmt = $pdo->prepare("DELETE FROM {$tabela} WHERE id = :id");
            return $stmt->execute(['id' => $id]);
        }
}
