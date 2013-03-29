==============
KXI
==============

:Author: Gao Peng <funky.gao@gmail.com>
:Description: 

.. contents:: Table Of Contents
.. section-numbering::


Diagram
=======

::


                      Engine o-----EngineProxy -----> other engine
                        |
                        | byName
                        |
                 +--------------------------+     |- StreamServer(listener) - handle(sock, addr)
                 |             |            |     |                              |
                Adapter     Adapter     Adapter o--- questQueue              conn_inboxQueue
                 |                                |
             +--------------+                     |- add_servant
             |              |
             | byName       | 
             |              |
          Servant       Servant


Queue
=====

::

            Adapter.handle
                |
                | produce
                V
            -----------
            quest queue
            -----------
                ^
                | consume
                |
            servant_worker(s)
                    |
                    | handle_normal_servant
                    |
                 callback = getattr(servant, quest.method)
                 result = callback(Params(quest.params, getattr(quest, 'ctx', None)))


Calling
=======

::


        Engine -> create_adapter
               -> serve_forever

        Adapter -> activate

        Servant.__init__ -> Adapter.add_servant


Housekeeping
============

::

        Adapter --- servant_worker
