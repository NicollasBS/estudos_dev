<?php

namespace App\Service;

use App\DTO\UserDto;
use App\Core\Repository;

class UserService{
    private const TABELA = 'users';

    public function getAllUsers(): array{
        return Repository::findAll(self::TABELA);
    }

    public function getUserById(int $id): mixed{
        $user = Repository::find(self::TABELA, $id);
        if(!$user){
            throw new \Exception('User not found', 404);
        }
        return $user;
    }

    public function createUser(UserDto $userDTO): string{
        $dados = [
            'nome' => $userDTO->nome,
            'idade' => $userDTO->idade,
        ];
        return Repository::insert(self::TABELA, $dados);
    }

    public function updateUser(UserDto $userDTO): bool {
        $dados = [
            'nome' => $userDTO->nome,
            'idade' => $userDTO->idade,
        ];
        return Repository::update(self::TABELA, $userDTO->id, $dados);
    }

    public function deleteUser(int $id): bool {
        // Primeiro, verifica se o usuário existe
        $this->getUserById($id);
        return Repository::delete(self::TABELA, $id);
    }
}
