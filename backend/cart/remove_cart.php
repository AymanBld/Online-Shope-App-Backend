<?php
include "../functions.php";

$productid = filterRequest('product_id');
$userid = filterRequest('user_id');


quary(
    "DELETE FROM `cart`
    WHERE `cart_user` = ? AND `cart_product` = ?",
    array($userid, $productid)
);