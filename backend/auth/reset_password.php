<?php

include "../functions.php";

$email = filterRequest('user_email');
$pass = sha1($_POST['user_pass']);

quary(
    "UPDATE `users` SET `user_pass` = ? WHERE `user_email` = ?",
    array($pass, $email)
);

?>