<?php
highlight_file('index.php');
$a=$_POST['level1'];
$b1=$_POST['level21'];
$b2=$_POST['level22'];

if(isset($a)&&!is_numeric($a)&&$a==520){
    if(isset($b1)&&isset($b2)&&$b1!==$b2&&md5($b1)==md5($b2)){
        echo "���سɹ������������㿩~";
        $re=$_POST['re'];
        $str=$_POST['str'];
        preg_replace(
        '/(' . $re . ')/ei',
        'strtolower("\\1")',
        $str
        );
    }
    else{
        die("���ͣ�");
    }
}
else{
    die("nonono��ŵ�һ�ذ�");
}

function getflag(){
    $cmd=$_GET['cmd'];
    if(preg_match('/(flag|cat|\*|system|tac|\\|`|\.)/i',$cmd)){
        die("����ư�");
    }
    eval($cmd);
}
?>