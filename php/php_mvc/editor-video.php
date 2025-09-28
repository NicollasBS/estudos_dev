<?php
$DB_HOST = 'localhost';
$DB_PORT = '5432';
$DB_NAME = 'php';
$DB_USER = 'php';
$DB_PASS = 'php';

$pdo = new PDO("pgsql:host=$DB_HOST;port=$DB_PORT;dbname=$DB_NAME;user=$DB_USER;password=$DB_PASS");
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

$stmt = $pdo->prepare('SELECT * FROM videos WHERE id = :id');
$stmt->execute(['id' => $_POST['id']]);
$video = $stmt->fetch(PDO::FETCH_ASSOC);

if (!$video) {
    header('HTTP/1.1 404 Not Found');
    exit;
}

if($_POST(''))
$video['']
?>
