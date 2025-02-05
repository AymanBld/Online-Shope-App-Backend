<?php
include "../../functions.php";

$productid = filterRequest('product_id');

quary(
    "DELETE FROM `products` WHERE `product_id` = ?",
    array($productid)
);