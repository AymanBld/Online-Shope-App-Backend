<?php

include "../../functions.php";

$email = filterRequest('delivery_email');
$verfiycode = rand(10000, 99999);

$data = quary(
    "SELECT * FROM `delivery` WHERE `delivery_email` = ?",
    array($email)
);

if (count($data) > 0) {
    quary(
        "UPDATE `deliverys` SET `delivery_verifycode` = ? WHERE `delivery_email` = ?",
        array($verfiycode, $email),
        false
    );
    sendemail();
}


?>