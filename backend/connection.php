<?php

$host = "localhost";
$dbname = "ecommerce";
$user = "root";
$pass = "";
$options = array(
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
);


try {
    $con = new PDO(
        "mysql:host=$host;dbname=$dbname",
        $user,
        $pass,
        $options
    );

} catch (PDOException $e) {
    echo $e->getMessage();
}



?>