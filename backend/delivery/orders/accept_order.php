<?php
include "../../functions.php";

$deliveryid = filterRequest('delivery_id');
$orderid = filterRequest('order_id');

quary(
    "UPDATE `orders` SET `orders`.`order_status`= 3 ,
    `orders`.`order_delivery` = ?
    WHERE `orders`.`order_id` = ?",
    array($deliveryid, $orderid)
);