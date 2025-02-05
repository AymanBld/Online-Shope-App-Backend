<?php
include "../functions.php";

$id = filterRequest('adr_id');

quary(
    "DELETE FROM `address` WHERE `address_id`= ?",
    array($id)
);