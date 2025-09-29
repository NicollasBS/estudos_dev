<?php

namespace App\Controller;

use App\DTO\UserDto;
use App\Service\UserService;
use App\Core\Response;

class UserController {
    private UserService $userService;

    public function __construct() {
        $this->userService = new UserService();
    }

    private function getJsonData(): array {
        return (array) json_decode(file_get_contents('php://input'), true);
    }

    public function index(): void {
        $users = $this->userService->getAllUsers();
        Response::json($users);
    }

    public function show(int $id): void {
        try {
            $user = $this->userService->getUserById($id);
            Response::json($user);
        } catch (\Exception $e) {
            Response::json(['error' => $e->getMessage()], $e->getCode() ?: 404);
        }
    }

    public function store(): void {
        $dados = $this->getJsonData();
        $userDTO = UserDto::fromRequest($dados);

        $userId = $this->userService->createUser($userDTO);

        Response::json(['message' => 'User created successfully', 'id' => $userId], 201);
    }

    public function update(int $id): void {
        $dados = $this->getJsonData();
        $userDTO = UserDto::fromRequest($dados, $id);

        $success = $this->userService->updateUser($userDTO);

        if ($success) {
            Response::json(['message' => "User {$id} updated successfully"]);
        } else {
            Response::json(['error' => "Failed to update user {$id}"], 500);
        }
    }

    public function destroy(int $id): void {
        try {
            $this->userService->deleteUser($id);
            Response::json(null, 204);
        } catch (\Exception $e) {
            Response::json(['error' => $e->getMessage()], $e->getCode() ?: 404);
        }
    }
}