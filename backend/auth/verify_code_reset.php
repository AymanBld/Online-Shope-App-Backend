<?php

include "../functions.php";

$email = filterRequest('user_email');
$verfiycode = filterRequest('user_verifycode');

quary(
    "SELECT * FROM `users` WHERE 
    `user_email` = ? AND `user_verifycode` = ? ",
    array($email, $verfiycode)
);


?>