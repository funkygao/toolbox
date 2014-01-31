<?php

$GLOBALS['THRIFT_ROOT'] = '/Users/gaopeng/github/thrift/lib/php/lib/Thrift';  
//require_once $GLOBALS['THRIFT_ROOT'].'/Thrift.php';
require_once '/Users/gaopeng/github/thrift/lib/php/src/Thrift.php';
require_once $GLOBALS['THRIFT_ROOT'].'/Protocol/TBinaryProtocol.php';
require_once $GLOBALS['THRIFT_ROOT'].'/Transport/TSocket.php';
require_once $GLOBALS['THRIFT_ROOT'].'/Transport/THttpClient.php';
require_once $GLOBALS['THRIFT_ROOT'].'/Transport/TBufferedTransport.php';

$GEN_DIR = './gen-php';  

require_once $GEN_DIR . '/HelloService.php';  
require_once $GEN_DIR . '/Types.php';  

// Set server host and port  
$host = "127.0.0.1";  
$port = 8787;  

try {
    //Thrift connection handling  
    $socket = new TSocket($host , $port );
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
