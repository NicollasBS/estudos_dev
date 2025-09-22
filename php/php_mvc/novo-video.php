<?php

$DB_HOST = 'localhost';
$DB_PORT = '5432';
$DB_NAME = 'php';
$DB_USER = 'php';
$DB_PASS = 'php';

$pdo = new PDO("pgsql:host=$DB_HOST;port=$DB_PORT;dbname=$DB_NAME;user=$DB_USER;password=$DB_PASS");
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

$url = filter_input(INPUT_POST, 'url', FILTER_VALIDATE_URL);
if($url === false){
    header('Location: /index.php?success=false');
    exit();
}
$titulo = filter_input(INPUT_POST, 'titulo', FILTER_SANITIZE_STRING);
if($titulo === false){
    header('Location: /index.php?success=false');
    exit();
}

$sql = 'INSERT INTO videos(url, titulo) VALUES (?, ?)';

$stmt = $pdo->prepare($sql);
$stmt->bindValue(1, $url);
$stmt->bindValue(2, $titulo);

if($stmt->execute() === false){
    header('Location: /index.php?success=false');
}else{
    header('Locarion: /index.php?success=true');
}

header('location: /index.php')

?>