<?php
include "../../functions.php";

$productid = filterRequest('product_id');
$name = filterRequest('pr_name');
$namear = filterRequest('pr_name_ar');
$description = filterRequest('pr_desc');
$descriptionar = filterRequest('pr_desc_ar');
$price = filterRequest('pr_price');
$discount = filterRequest('pr_discount');
$categorie = filterRequest('pr_categorie');
$image;

quary(
    "UPDATE `products` SET 
    `product_name`= ?,`product_name_ar`= ?,`product_description`= ?,
    `product_description_ar`= ?, `product_image`= ?, `product_price`= ?,
    `product_discount`= ?, `product_categorie`= ?
    WHERE `product_id` = ?",
    array($name, $namear, $description, $descriptionar, $image, $price, $discount, $categorie, $productid)
);