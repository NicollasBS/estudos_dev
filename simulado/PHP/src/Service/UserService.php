<?php

namespace App\Service;

use App\DTO\UserDto;
use App\Repository\UserRepository;

class UserService{
    private UserRepository $userRepository;

    public function __construct(){
        $this->userRepository = new UserRepository();
    }

    public function getAllUsers(): array{
        return $this->userRepository->findAll();
    }

    public function getUserById(int $id): mixed{
        $user = $this->userRepository->find($id);
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
        return $this->userRepository->insert($dados);
    }

    public function updateUser(UserDto $userDTO): bool {
        $dados = [];
        if($userDTO->nome !== null){
            $dados['nome'] = $userDTO->nome;
        }
        if($userDTO->idade !== null){
            $dados['idade'] = $userDTO->idade;
        }
        return $this->userRepository->update($userDTO->id, $dados);
    }

    public function deleteUser(int $id): bool {
        $this->getUserById($id);
        return $this->userRepository->delete($id);
    }
}