<?php
session_start();
$flag=getenv("GZCTF_FLAG");

if (!isset($_SESSION['score'])) {
    $_SESSION['score'] = 0;
}

if (isset($_POST['score'])) {
    $_SESSION['score'] = intval($_POST['score']);
    if ($_SESSION['score'] >= 10000000000) {
        echo "恭喜你获得了10000000000分！Flag: $flag";
        exit();
    }
}
?>