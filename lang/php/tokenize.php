<?php
// demo how php zend engine lex a src file

$src = '<?php echo "hello world";';
$t = token_get_all($src);
foreach ($t as $token) {
    if (is_array($token)) {
        echo token_name($token[0]) . "({$token[2]}) - {$token[1]}\n";
    } else {
        echo "{$token}\n";
    }
}
