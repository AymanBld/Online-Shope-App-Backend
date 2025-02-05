<?php

include "../functions.php";

$email = filterRequest('user_email');
$pass = sha1($_POST['user_pass']);


quary(
    "SELECT * FROM `users` WHERE
    `user_email` = ? AND `user_pass` = ? ",
    array($email, $pass)
);

?>