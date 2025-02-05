<?php
include "../../functions.php";



quary(
    "SELECT `orders`.*, `users`.*,`address`.`address_name`
    FROM `orders`, `address`, `users`
    WHERE `orders`.`order_user` = `users`.`user_id`
    AND `orders`.`order_status` = 2
    AND `orders`.`order_address` = `address`.`address_id`",
    array()
);