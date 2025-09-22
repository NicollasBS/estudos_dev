<?php

$DB_HOST = 'localhost';
$DB_PORT = '5432';
$DB_NAME = 'php';
$DB_USER = 'php';
$DB_PASS = 'php';

$pdo = new PDO("pgsql:host=$DB_HOST;port=$DB_PORT;dbname=$DB_NAME;user=$DB_USER;password=$DB_PASS");
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

$id = $_GET['id'];

$sql = "DELETE FROM videos WHERE id = ?";
$stmt = $pdo->prepare($sql);
$stmt->bindValue(1, $id);

if($stmt->execute() === false){
    header('Location: /index.php?success=false');
}else {
    header('Location: /index.php?success=true');
}