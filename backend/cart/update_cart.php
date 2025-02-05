<?php
include "../functions.php";

$productid = filterRequest('product_id');
$userid = filterRequest('user_id');
$contity = filterRequest('product_contity');

quary(
    "INSERT INTO `cart` (`cart_user`, `cart_product`,`cart_pr_contity`)
    VALUES ($userid, $productid, $contity)
    ON DUPLICATE KEY
    UPDATE `cart_pr_contity`= `cart_pr_contity` + $contity;",
    array()
);

