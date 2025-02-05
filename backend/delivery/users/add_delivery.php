<?php

include "../../functions.php";


$deliveryname = filterRequest('delivery_name');
$email = filterRequest('delivery_email');
$phone = filterRequest('delivery_phone');
$pass = sha1($_POST['delivery_pass']);
$verfiycode = rand(10000, 99999);

$data = quary(
    "SELECT * FROM delivery WHERE delivery_email = ? OR delivery_phone = ? ",
    array($email, $phone),
    false
);

if (count($data) > 0) {
    printfailed();
} else {
    quary(
        "INSERT INTO `delivery`
        (`delivery_name`, `delivery_email`, `delivery_pass`, `delivery_phone`, `delivery_verifycode`)
        VALUES (?, ?, ?, ?, ?)"
        ,
        array($deliveryname, $email, $pass, $phone, $verfiycode)
    );
    sendemail();
}




?>