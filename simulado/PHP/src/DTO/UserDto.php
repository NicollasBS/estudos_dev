<?php

namespace App\DTO;

class UserDto {
    public readonly ?int $id;
    public readonly ?string $nome;
    public readonly ?int $idade;

    public function __construct(?int $id, ?string $nome, ?int $idade){
        $this->id = $id;
        $this->nome = $nome;
        $this->idade = $idade;
    }

    public static function fromRequest(array $data, ?int $id = null): self{
        return new self(
            $id,
            $data['nome'] ?? null,
            isset($data['idade']) ? (int) $data['idade'] : null
        );
    }
}