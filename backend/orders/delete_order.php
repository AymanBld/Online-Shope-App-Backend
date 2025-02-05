<?php
include "../functions.php";

$orderid = filterRequest('order_id');

quary(
    "DELETE FROM `orders`
    WHERE `order_id` = ?",
    array($orderid)
);