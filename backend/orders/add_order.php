<?php
include "../functions.php";

$userid = filterRequest('user_id');
$price = filterRequest('order_price');
$count = filterRequest('order_count');
$payment = filterRequest('order_payment');
$address = filterRequest('order_address');

quary(
    "INSERT INTO `orders`(`order_user`, `order_price`, `order_count`, `order_payement`, `order_address`)
    VALUES (?,?,?,?,?)",
    array($userid, $price, $count, $payment, $address),
    false
);

quary(
    "UPDATE `cart`
        SET `cart_order` = (SELECT MAX(`order_id`) FROM `orders`)
        WHERE `cart_order` = 0
        AND `cart_user` = ?",
    array($userid)
);


