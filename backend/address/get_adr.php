<?php
include "../functions.php";

$userid = filterRequest('user_id');

quary(
    "SELECT * FROM `address` WHERE `address_user` = ?",
    array($userid)
);