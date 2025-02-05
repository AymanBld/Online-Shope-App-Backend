<?php
include "../../functions.php";

$productid = filterRequest('categorie_id');

quary(
    "DELETE FROM `categories` WHERE `categorie_id` = ?",
    array($productid)
);