<?php
include "../../functions.php";

$categoryid = filterRequest('category_id');
$name = filterRequest('category_name');
$namear = filterRequest('category_name_ar');
$image;

quary(
    "UPDATE `categories` SET `categorie_name`= ?,`categorie_name_ar`= ?,`categorie_image`= ?
    WHERE `categorie_id` = ?",
    array($name, $namear, $image, $categoryid)
);