<?php
namespace App\Core;

class Response {
    public static function json(mixed $data, int $statusCode = 200): void{
        header('Content-Type: application/json; charset=utf-8');
        http_response_code($statusCode);
        if($statusCode !== 204){
            echo json_encode($data);
        }
        exit();
    }
}
