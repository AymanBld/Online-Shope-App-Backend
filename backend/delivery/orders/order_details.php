<?php
include "../functions.php";

$orderid = filterRequest('order_id');

quary(
    "SELECT * FROM `ordersview`
    WHERE `order_id` = ?",
    array($orderid)
);