<?php
include "../functions.php";


$namesearch = filterRequest('name_search');
$userid = filterRequest('user_id');


quary(
    "SELECT `productview`.*, 1 as `isfavorite`
    FROM `productview`,`favorite`
    WHERE  `productview`.`product_id` = `favorite`.`fav_product`
    AND `favorite`.`fav_user` = $userid
    AND (`product_name` LIKE '%$namesearch%'
    OR `product_name_ar` LIKE '%$namesearch%') 
    
    UNION ALL
    SELECT * , 0 as `isfavorite` FROM `productview` 
    WHERE  (`product_name` LIKE '%$namesearch%'
    OR `product_name_ar` LIKE '%$namesearch%')
    AND `product_id` NOT IN (SELECT `productview`.`product_id`
    FROM `productview`,`favorite`
    WHERE `productview`.`product_id` = favorite.fav_product
    AND favorite.fav_user = $userid)",
    array()
);
