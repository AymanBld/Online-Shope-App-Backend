<?php

include "../functions.php";

$email = filterRequest('user_email');
$verfiycode = rand(10000, 99999);

$data = quary(
    "SELECT * FROM `users` WHERE `user_email` = ?",
    array($email)
);

if (count($data) > 0) {
    quary(
        "UPDATE `users` SET `user_verifycode` = ? WHERE `user_email` = ?",
        array($verfiycode, $email),
        false
    );
    sendemail();
}


?>