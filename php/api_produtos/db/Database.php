<?php

class Database{
    private const DB_HOST = 'localhost';
    private const DB_NAME = 'php';
    private const DB_PORT = '5432';
    private const DB_USER = 'php';
    private const DB_PASS = 'php';

    private static ?PDO $instance = null;

    private function __construct(){}
    private function __clone(){}

    public static function getInstance(): PDO{
        if(self::$instance === null){
            $dsn = 'pgsql:host=' . self::DB_HOST . ';port=' . self::DB_PORT . ';dbname=' . self::DB_NAME;

            try {
                self::$instance = new PDO($dsn, self::DB_NAME, self::DB_PASS);
                self::$instance->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

                self::createProdutoTable();
            } catch (PDOException $e) {
                die("Erro de conexão com o PostgreSQL: " . $e->getMessage());
            }
        }

        return self::$instance;
    }

    private static function createProdutoTable(): void{
        $query = "
            CREATE TABLE IF NOT EXISTS produtos(
                id SERIAL PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                preco NUMERIC(10,2) NOT NULL
            );
        ";

        try{
            self::getInstance()->exec($query);
        } catch (PDOException $e){
            die("Erro ao criar tabela 'produtos' : " . $e->getMessage());
        }
    }

}

?>
