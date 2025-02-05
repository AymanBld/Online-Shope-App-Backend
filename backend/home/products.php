<?php
include "../functions.php";

$categoryid = filterRequest('category_id');
$userid = filterRequest('user_id');


quary(
    "SELECT `productview`.*, 1 as `isfavorite` FROM `productview`,`favorite`
    WHERE `productview`.`product_id` = `favorite`.`fav_product` 
    AND `favorite`.`fav_user` = :user AND `productview`.`categorie_id` = :cat

    UNION ALL
    SELECT * , 0 as `isfavorite` FROM `productview` 
    WHERE  `productview`.`categorie_id` = :cat AND
    `product_id` NOT IN (SELECT `productview`.`product_id` FROM `productview`,`favorite`
    WHERE `productview`.`product_id` = favorite.fav_product AND favorite.fav_user = :user)",

    array(
        ':user' => $userid,
        ':cat' => $categoryid
    )
);