<?php
highlight_file('index.php');
$a=$_POST['level1'];
$b1=$_POST['level21'];
$b2=$_POST['level22'];

if(isset($a)&&!is_numeric($a)&&$a==520){
    if(isset($b1)&&isset($b2)&&$b1!==$b2&&md5($b1)==md5($b2)){
        echo "闯关成功！接下来靠你咯~";
        $re=$_POST['re'];
        $str=$_POST['str'];
        preg_replace(
        '/(' . $re . ')/ei',
        'strtolower("\\1")',
        $str
        );
    }
    else{
        die("加油！");
    }
}
else{
    die("nonono这才第一关啊");
}

function getflag(){
    $cmd=$_GET['cmd'];
    if(preg_match('/(flag|cat|\*|system|tac|\\|`|\.)/i',$cmd)){
        die("随便绕啊");
    }
    eval($cmd);
}
?>