=======================
verify / token
=======================

:Author: Gao Peng <funky.gao@gmail.com>

.. contents:: Table Of Contents
.. section-numbering::

::

    list($uid, $aid, $_uid, $time, $md5) = explode("_", $this->verify, 5);

    function getVerify($uid, $aid, $vuid, $verifycode, $userverify="", $timespan=1) {
        $now = time();
        if ($timespan > 1) {
            $now -= $now % intval($timespan);
        }
        $userverify = CUtils::getInstance("CUser")->getVerifycode($vuid);
        return $uid.
            "_".$aid.
            "_".$vuid.
            "_".$now.
            "_".
            md5($aid."_".$vuid."_".$now."_".$verifycode."_".$userverify);
    }
