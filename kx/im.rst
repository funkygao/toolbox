=========================
web IM implementation
=========================

:Author: Gao Peng <gaopeng@corp.kaixin001.com>
:Revision: $Id$


::



                                    ajaxPost
                    MsgFrame.js.gb ----->---- /home/newmsg.php?im=1
                         |                            |
                         |                            V
                         |                   {
                         |                      vuid: 9940649,
                         |                      imseq: 0,
                         |                      imweb: 'm222033',
                         |                      kxi_imweb: '',
                         |                      prstate: {
                         |                          notice: 0,
                         |                          msg: 0,
                         |                          sysmsg: 0,
                         |                          bbs: 0,
                         |                          comment: 0,
                         |                          reply: 0,
                         |                          rgroupmsg: 0,
                         |                          online: '',
                         |                          forbidsound: 0,
                         |                          kxt: 0,
                         |                          kxg: 1
                         |                      },
                         |                      t: 'init'
                         |                   }
                         |
                         | got target(IM server = m222033)
                         |
                    create <iframe id='presence_iframe' src='http://m222033.kaixin001.com/ifr/js?r=http://s.kaixin001.com.cn/js/forks/home/kxbase-0029ec281.js&r=http://s.kaixin001.com.cn/js/IMPresence-0002e1c89.js' />
                         |
                         | K.fireReady( 'msg:init_ok', data );
                         |
                    load IMPresence.js
                         |
                         | on('msg:init_ok')
                         |
                         |         GET
                    presence_init -->-- http://m222033.kaixin001.com/g/0.4198129454161972/9940649/ctx
                         |                  |
                         |                  V
                         |              {t:'ctx', seq:28, ctx:{state:{notice:0,msg:0,sysmsg:0,bbs:0,...}}}
                         |
                    presence_getseq --- get the seq
                         |
                         |          GET
                    presence_query -->-- http://m222033.kaixin001.com/k/0.05611203587614/9940649/29
                                            |
                    presence_show           |
                         |                  V
                         ^                  |
                         |         response |
                --------------------------------
               |                                |
             refresh                          inform
               |                                | {t:'inform', infos:[{t:1343356614, c:'.user.online', o:{uid:83803119}}]}
               |                                | {t:'inform', infos:[{t:1343356614, c:'.ctx', o:{...}}]}
               V {t: 'refresh', seq: 29}        V {t:'inform', infos:[{t:1343356614, c:'msg.clearblink', o:{blink:0}}]}
               |                                | {t:'inform', infos:[{t:1343356614, c:'.user.offline', o:{uid:83803119}}]}
               |                                |
             get new seq                    fire events and try again

