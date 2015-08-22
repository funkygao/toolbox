<?php

// innodb_support_xa=ON
// tx_isolation=SERIALIZABLE

$foo = new mysqli("10.77.145.36","root","root","db1") or die("$foo：连接失败");
$map = new mysqli("10.77.145.36","root","root","db2") or die("$map：连接失败");

$grid = uniqid(""); // xid
echo "grxid:", $grid, "\n";

// 1pc start
$map->query("XA START '$grid'");//准备事务1
$foo->query("XA START '$grid'");//准备事务2
echo "XA START done\n";

try {
    $return = $map->query("UPDATE test_transation2 SET name='foo' WHERE id=2") ; //第一个分支事务准备做的事情，通常他们会记录进日志
    if($return == false) {
        throw new Exception("map");
    }

    $return = $foo->query("UPDATE test_transation1 SET name='bar' WHERE id=1"); //第二个分支事务准备做的事情，通常他们会记录进日志
    if($return == false) {
        throw new Exception("foo");
    }

    // 1pc end
    $map->query("XA END '$grid'");
    $foo->query("XA END '$grid'");

    // 2pc prepare
    $map->query("XA PREPARE '$grid'");
    $foo->query("XA PREPARE '$grid'");

    // 2pc commit
    $foo->query("XA COMMIT '$grid'");
    $map->query("XA COMMIT '$grid'");
} catch (Exception $e) {
    echo "rollback...\n";
    $foo->query("XA ROLLBACK '$grid'");
    $map->query("XA ROLLBACK '$grid'");
    print $e->getMessage();
}

$map->close();
$foo->close();
