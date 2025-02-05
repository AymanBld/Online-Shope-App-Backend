<?php
include "../functions.php";

$productid = filterRequest('product_id');
$userid = filterRequest('user_id');

quary(
    "INSERT INTO `favorite` (`fav_user`, `fav_product`) VALUES (?, ?)",
    array($userid, $productid)
);