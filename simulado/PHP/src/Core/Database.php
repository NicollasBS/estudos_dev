<?php

namespace App\Core;

use \PDO;
use \PDOException;

class Database{
    private static ?PDO $instance = null;

    private function __construct(){}

    private function __clone(){}

    public static function getInstance(): PDO{
        if(self::$instance === null){
            $dsn = DB_DRIVER . ':host=' . DB_HOST . ';port=' . DB_PORT . ';dbname=' . DB_NAME;

            $options = [
                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                PDO::ATTR_EMULATE_PREPARES => false
            ];

            try{
                self::$instance = new PDO($dsn, DB_USER, DB_PASS, $options);
            }catch (PDOException $e){
                throw new PDOException($e->getMessage(), (int) $e->getCode());
            }
        }

        return self::$instance;
    }
}