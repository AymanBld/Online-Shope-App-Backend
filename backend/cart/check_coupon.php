<?php
include "../functions.php";


$coupon = filterRequest('coupon_name');
$dateNow = date('y-m-d');

quary(
    "SELECT * FROM `coupon`
        WHERE `coupon_name` = ? AND coupon_contity > 0
        AND `coupon_date_ex` > ? ",
    array($coupon, $dateNow)
);