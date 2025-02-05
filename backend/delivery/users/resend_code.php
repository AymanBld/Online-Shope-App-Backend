<?php

include "../../functions.php";

$code = rand(10000, 99999);
$deliveryemail = filterRequest("delivery_email");

quary(
    "UPDATE `delivery` SET `delivery_verifycode` = ? WHERE `delivery_email` = ?",
    array($code, $deliveryemail)
);

sendemail();