<?php
function cookieFile($url, $account = 'royalAdmin') {
    $urlScheme = parse_url($url);
    return 'tmp/cookie_' . $urlScheme['host'] . '_' . $account;
}

function httpPost($url, $postData = '', $idcookie = false, $quiet = false) {
    $_SESSION = array('account'=>'royalAdmin');

    if (is_array($postData)) {
        foreach ($postData as $key => $value) {
            if ($value != null) {
                @ $fields_string .= $key . '=' . $value . '&';
            } else {
                @ $fields_string .= $key . '&';
            }
        }
        rtrim($fields_string, '&');
        $postData = $fields_string;
    }
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_HEADER, false);
    curl_setopt($ch, CURL_HTTP_VERSION_1_1, true);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_AUTOREFERER, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_POST, count($postData));
    curl_setopt($ch, CURLOPT_TIMEOUT, 45);
    curl_setopt($ch, CURLOPT_MAXREDIRS, 10);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $postData);
    curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (X11; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0');
    curl_setopt($ch, CURLOPT_COOKIESESSION, true );
    if ($idcookie) {
        curl_setopt($ch, CURLOPT_COOKIEJAR, cookieFile($url, $_SESSION['userId']));
        curl_setopt($ch, CURLOPT_COOKIEFILE, cookieFile($url, $_SESSION['userId']));
    } else {
        curl_setopt($ch, CURLOPT_COOKIEJAR, cookieFile($url, $_SESSION['account']));
        curl_setopt($ch, CURLOPT_COOKIEFILE, cookieFile($url, $_SESSION['account']));
    }

    curl_setopt($ch, CURLOPT_ENCODING, 'gzip');
    curl_setopt($ch, CURLOPT_HTTPHEADER, array (
        'Accept-Language: en-US',
        'Pragma: no-cache'
    ));
    if (@ $_SESSION['use_proxy']) {
        curl_setopt($ch, CURLOPT_PROXY, trim($_SESSION['proxy_settings'][0] . ':' . $_SESSION['proxy_settings'][1]));
        curl_setopt($ch, CURLOPT_PROXYPORT, intval($_SESSION['proxy_settings'][1]));
        if (isset ($_SESSION['proxy_settings'][2]) && isset ($_SESSION['proxy_settings'][3])) { // is set proxy user and password
            $authorization = trim($_SESSION['proxy_settings'][2]) . ':' . trim($_SESSION['proxy_settings'][3]);
            curl_setopt($ch, CURLOPT_PROXYUSERPWD, $authorization);
            curl_setopt($ch, CURLOPT_PROXYAUTH, CURLAUTH_BASIC);
        }
    }
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    if ($httpCode == 404) {
        if (!$quiet) OutputLog("faceBot Web IO: Error 404/Page Not Found");
        return;
    }
    if ($httpCode == 500) {
        if (!$quiet) OutputLog("faceBot Web IO: Error 500/Internal Server Error");
        return;
    }
    if (empty ($response)) {
        if (!$quiet) OutputLog("faceBot Web IO: Empty Response Returned");
        return;
    }
    curl_close($ch);
    return $response;
}

function httpGet($url = '', $idcookie = false, $timeout = true, $quiet = false) {
    $_SESSION = array('account'=>'royalAdmin');

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_HEADER, 0);
    //curl_setopt($ch, CURL_HTTP_VERSION_1_1, true);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_AUTOREFERER, true);
    if ($timeout) curl_setopt($ch, CURLOPT_TIMEOUT, 45);
    //curl_setopt($ch, CURLOPT_MAXREDIRS, 10);
    curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (Windows NT 5.1; rv:6.0.2) Gecko/20100101 Firefox/6.0.2');
    if ($idcookie) {
        curl_setopt($ch, CURLOPT_COOKIEJAR, @$_SESSION['base_path'] . $_SESSION['userId'] . '_fbcookie');
        curl_setopt($ch, CURLOPT_COOKIEFILE, @$_SESSION['base_path'] . $_SESSION['userId'] . '_fbcookie');
        curl_setopt($ch, CURLOPT_COOKIEJAR, cookieFile($url, $_SESSION['userId']));
        curl_setopt($ch, CURLOPT_COOKIEFILE, cookieFile($url, $_SESSION['userId']));
    } else {
        curl_setopt($ch, CURLOPT_COOKIEJAR, cookieFile($url, $_SESSION['account']));
        curl_setopt($ch, CURLOPT_COOKIEFILE, cookieFile($url, $_SESSION['account']));
    }
    curl_setopt($ch, CURLOPT_ENCODING, 'gzip');
    curl_setopt($ch, CURLOPT_HTTPHEADER, array (
        'Accept-Language: en-US',
        'Pragma: no-cache'
    ));
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    if ($httpCode == 404) {
        if (!$quiet) OutputLog("faceBot Web IO: Error 404/Page Not Found");
        return;
    }
    if ($httpCode == 500) {
        if (!$quiet) OutputLog("faceBot Web IO: Error 500/Internal Server Error");
        return;
    }
    if (empty ($response)) {
        if (!$quiet) OutputLog("faceBot Web IO: Empty Response Returned");
        return;
    }
    curl_close($ch);
    return $response;
}

