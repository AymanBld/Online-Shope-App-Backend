<?php
include "../functions.php";

$productid = filterRequest('product_id');
$userid = filterRequest('user_id');

quary(
    "DELETE FROM `favorite`
        WHERE `fav_user`= ? AND `fav_product` = ?",
    array($userid, $productid)
);