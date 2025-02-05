<?php

include "../functions.php";

$code = rand(10000, 99999);
$useremail = filterRequest("user_email");

quary(
    "UPDATE `users` SET `user_verifycode` = ? WHERE `user_email` = ?",
    array($code, $useremail)
);

sendemail();