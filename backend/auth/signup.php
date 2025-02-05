<?php

include "../functions.php";


$username = filterRequest('user_name');
$email = filterRequest('user_email');
$phone = filterRequest('user_phone');
$pass = sha1($_POST['user_pass']);
$verfiycode = rand(10000, 99999);

$data = quary(
    "SELECT * FROM users WHERE user_email = ? OR user_phone = ? ",
    array($email, $phone),
    false
);

if (count($data) > 0) {
    printfailed();
} else {
    quary(
        "INSERT INTO `users`
        (`user_name`, `user_email`, `user_pass`, `user_phone`, `user_verifycode`)
        VALUES (?, ?, ?, ?, ?)"
        ,
        array($username, $email, $pass, $phone, $verfiycode)
    );
    sendemail();
}




?>