<?php
include "../functions.php";

$userid = filterRequest('user_id');


quary(
    "SELECT `orders`.*, `address`.`address_name`
    FROM `orders`, `address`
    WHERE `order_user` = ?
    AND `order_status` = 4
    AND `orders`.`order_address` = `address`.`address_id`;",
    array($userid)
);