<?php

$GLOBALS['THRIFT_ROOT'] = '/opt/app/thrift/lib/php';
require_once $GLOBALS['THRIFT_ROOT'].'/Thrift.php';
require_once $GLOBALS['THRIFT_ROOT'].'/Protocol/TBinaryProtocol.php';
require_once $GLOBALS['THRIFT_ROOT'].'/Transport/TSocket.php';
require_once $GLOBALS['THRIFT_ROOT'].'/Transport/THttpClient.php';
require_once $GLOBALS['THRIFT_ROOT'].'/Transport/TBufferedTransport.php';

$GEN_DIR = './gen-php';  

require_once $GEN_DIR . '/HelloService.php';  
require_once $GEN_DIR . '/Types.php';  

try {
    $socket = new TSocket('localhost', 8787);
    $transport = new TBufferedTransport($socket, 1024, 1024);
    $protocol = new TBinaryProtocol($transport);

    // get our client
    $client = new HelloServiceClient($protocol);
    $transport->open();

    $return = $client->hello_func();
    echo $return;

    $transport->close();
} catch (TException $tx) {
    print 'Something went wrong: ' . $tx->getMessage() . "\n";
}
