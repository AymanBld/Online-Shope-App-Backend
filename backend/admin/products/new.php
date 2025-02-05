<?php
include "../../functions.php";

$name = filterRequest('product_id');
$namear = filterRequest('user_id');
$description = filterRequest('user_id');
$descriptionar = filterRequest('user_id');
$price = filterRequest('user_id');
$discount = filterRequest('user_id');
$categorie = filterRequest('user_id');
$image;

quary(
    "INSERT INTO `products` (`product_name`, `product_name_ar`,
    `product_description`, `product_description_ar`, `product_image`,
    `product_price`, `product_discount`, `product_categorie`)
    VALUES (?,?,?,?,?,?,?,?)",
    array($name, $namear, $description, $descriptionar, $image, $price, $discount, $categorie)
);