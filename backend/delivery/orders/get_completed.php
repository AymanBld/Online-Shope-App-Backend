<?php
include "../../functions.php";

$deliveryid = filterRequest('delivery_id');

quary(
    "SELECT `orders`.*, `address`.`address_name`
    FROM `orders`, `address`
    WHERE `orders`.`order_status` = 4
    AND `orders`.`order_delivery` = ?
    AND `orders`.`order_address` = `address`.`address_id`;",
    array($deliveryid)
);