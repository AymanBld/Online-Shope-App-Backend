<?php
include "../../functions.php";

$name = filterRequest('category_name');
$namear = filterRequest('category_name_ar');
$image;

quary(
    "INSERT INTO `categories`(`categorie_name`, `categorie_name_ar`, `categorie_image`)
    VALUES (?,?,?)",
    array($name, $namear, $image)
);