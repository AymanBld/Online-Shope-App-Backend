<?php

include "../../functions.php";

$email = filterRequest('delivery_email');
$pass = sha1($_POST['delivery_pass']);

quary(
    "UPDATE `delivery` SET `delivery_pass` = ? WHERE `delivery_email` = ?",
    array($pass, $email)
);

?>