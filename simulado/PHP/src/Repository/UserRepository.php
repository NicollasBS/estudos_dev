<?php
namespace App\Repository;
use App\Core\BaseRepository;


class UserRepository extends BaseRepository{
    protected string $tabela = 'users';

    public function findByNome($nome): array{
        $stmt = $this->pdo->prepare("SELECT * FROM {$this->tabela} WHERE nome = :nome");
        $stmt->execute(['nome' => "%{$nome}%"]);
        return $stmt->fetchAll();
    }
}