<?php
include "../functions.php";

$data = array();


$data['status'] = 'success';

$categories = quary(
    "SELECT * FROM `categories`",
    array(),
    false
);
$data['categories'] = $categories;

$products = quary(
    "SELECT * FROM `productview` WHERE `product_discount` != 0",
    array(),
    false
);
$data['products'] = $products;




echo json_encode($data);

?>