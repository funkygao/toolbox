<?php
include 'lib.php';

$servers = array(
    'us' => array(
        'login_url' => 'http://54.245.252.91/tools/login.php',
        'dashboard_url' => 'http://54.245.252.91/tools/main/?',
    ),
    'ae' => array(
        'login_url' => 'http://royal-ae.socialgamenet.com//tools/login.php',
        'dashboard_url' => 'http://royal-ae.socialgamenet.com/tools/main/?',
    ),
    'nl' => array(
        'login_url' => 'http://royal-nl.socialgamenet.com//tools/login.php',
        'dashboard_url' => 'http://royal-nl.socialgamenet.com/tools/main/?',
    ),
    'de' => array(
        'login_url' => 'http://royal-de.socialgamenet.com//tools/login.php',
        'dashboard_url' => 'http://royal-de.socialgamenet.com/tools/main/?',
    ),
    'fr' => array(
        'login_url' => 'http://royal-fr.socialgamenet.com//tools/login.php',
        'dashboard_url' => 'http://royal-fr.socialgamenet.com/tools/main/?',
    ),
    'th' => array(
        'login_url' => 'http://royal-th.socialgamenet.com//tools/login.php',
        'dashboard_url' => 'http://royal-th.socialgamenet.com/tools/main/?',
    ),
    /*
    'spil' => array(
        'login_url' => 'http://royal-spilgames.socialgamenet.com//tools/login.php',
        'dashboard_url' => 'http://royal-spilgames.socialgamenet.com/tools/main/?',
        'account' => 'rock',
        'pass' => 'royalbeyondfarm',
    ),
     */
);

function runAll() {
    global $servers;


    file_put_contents('var/locales', json_encode(array_keys($servers)));

    foreach ($servers as $locale=>$server) {
        $account = 'royalAdmin';
        $pass = 'royalPass';
        if (!empty($server['account'])) {
            $account = $server['account'];
            $pass = $server['pass'];
        }
        httpPost($server['login_url'], array('account'=> $account, 'password'=> $pass, 'submit'=>true));
        $dashboard = httpGet($server['dashboard_url'], array());
        preg_match('/var statisDatas = ([^;]*);/sim', $dashboard, $data);
        $dataArray = json_decode($data[1], true);
        handleData($locale, $dataArray);
    }
}

function handleData($locale, $datas) {
    foreach ($datas as $k => $v) {
        file_put_contents('var/' . $locale . '_' . $k, json_encode($v));
    }
}


runAll();
