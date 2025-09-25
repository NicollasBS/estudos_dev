<?php
namespace App\Model\User;
class User{
    private string $nome;
    private int $idade;

    public function getNome(): string {
            return $this->nome;
        }

        public function setNome(string $nome): void {
            $this->nome = $nome;
        }

        public function getIdade(): int {
            return $this->idade;
        }

        public function setIdade(int $idade): void {
            $this->idade = $idade;
        }
}
