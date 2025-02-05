<?php
include "../functions.php";

$name = filterRequest('adr_name');
$city = filterRequest('adr_city');
$street = filterRequest('adr_street');
$lat = filterRequest('adr_lat');
$long = filterRequest('adr_long');
$userid = filterRequest('adr_user');


quary(
    "INSERT INTO `address`(`address_name`,`address_city`,
    `address_street`, `address_lang`, `address_lat`, `address_user`)
    VALUES (?,?,?,?,?,?)",
    array($name, $city, $street, $lat, $long, $userid)
);