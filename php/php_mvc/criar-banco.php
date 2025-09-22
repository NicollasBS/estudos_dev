<?php

$DB_HOST = 'localhost';
$DB_PORT = '5432';
$DB_NAME = 'php';
$DB_USER = 'php';
$DB_PASS = 'php';

$pdo = new PDO("pgsql:host=$DB_HOST;port=$DB_PORT;dbname=$DB_NAME;user=$DB_USER;password=$DB_PASS");
$pdo->exec('CREATE TABLE IF NOT EXISTS videos(id SERIAL PRIMARY KEY, url VARCHAR(255), titulo VARCHAR(255));');




?>