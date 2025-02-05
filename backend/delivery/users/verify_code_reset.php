<?php

include "../../functions.php";

$email = filterRequest('delivery_email');
$verfiycode = filterRequest('delivery_verifycode');

quary(
    "SELECT * FROM `delivery` WHERE 
    `delivery_email` = ? AND `delivery_verifycode` = ? ",
    array($email, $verfiycode)
);


?>