<?php

include "../../functions.php";

$email = filterRequest('delivery_email');
$pass = sha1($_POST['delivery_pass']);


quary(
    "SELECT * FROM `delivery` WHERE
    `delivery_email` = ? AND `delivery_pass` = ? ",
    array($email, $pass)
);

?>