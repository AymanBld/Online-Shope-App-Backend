<?php

include "../functions.php";

$email = filterRequest('user_email');
$verfiycode = filterRequest('user_verifycode');

$data = quary(
    "SELECT * FROM `users` WHERE 
    `user_email` = ? AND `user_verifycode` = ? ",
    array($email, $verfiycode),
    false
);

if (count($data) > 0) {
    quary(
        "UPDATE `users`
        SET `user_verifyed` = 1 WHERE `user_email` = ?",
        array($email)
    );
} else {
    printfailed();
}



?>