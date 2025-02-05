<?php
include "connection.php";

function quary($sql, $argms, $json = true)
{
    global $con;
    $stmt = $con->prepare($sql);
    $stmt->execute($argms);
    $data = $stmt->fetchAll();

    if ($json == true) {
        if ($stmt->rowCount() > 0) {
            printsuccess($data);
        } else {
            printfailed();
        }
    }
    return $data;
}
function printsuccess($message = 'no data')
{
    echo json_encode(
        array(
            "status" => "success",
            "data" => $message
        )
    );
}
function printfailed($message = 'failed')
{
    echo json_encode(
        array(
            "status" => "failed",
            "message" => $message
        )
    );
}
function filterRequest($request)
{
    return htmlspecialchars(strip_tags($_POST[$request]));

}
function sendemail()
{

}
