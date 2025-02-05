<?php
include "../functions.php";

$userid = filterRequest('user_id');

$totalData = quary(
    "SELECT SUM(`product_discount_price` * `cart_pr_contity`) as `total_price`,
    COUNT(`cartview`.`product_id`) AS `total_count`
    FROM `cartview`
    WHERE `cartview`.`cart_user` = ?",
    array($userid),
    false
);

$cartData = quary(
    "SELECT * FROM `cartview`
    WHERE `cart_user` = ?",
    array($userid),
    false
);

if (count($cartData) > 0) {
    echo json_encode(
        array(
            "status" => "success",
            "data" => $cartData,
            "total_price" => $totalData[0]['total_price'],
            "total_count" => $totalData[0]['total_count'],
        )
    );
} else {
    printfailed();
}
