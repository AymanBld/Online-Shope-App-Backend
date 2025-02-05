<?php
include "../functions.php";


$userid = filterRequest('user_id');

quary(
    "SELECT `productview`.* , 1 as `isfavorite`
    FROM `productview`, `favorite`
    WHERE `productview`.`product_id` = `favorite`.`fav_product`
    AND `favorite`.`fav_user` = ?",
    array($userid)
);