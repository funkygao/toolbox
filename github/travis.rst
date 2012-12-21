=========================
travis CI in github
=========================

:Author: Gao Peng <funky.gao@gmail.com>

.. contents:: Table Of Contents
.. section-numbering::

.travis.yml
============

::

    language: go
    install:
      - go get github.com/bmizerany/assert
      - go get github.com/bitly/go-notify
      - go get github.com/bitly/go-simplejson
    script: ./test.sh
    notifications:
      email: false


TravisCI
========

P = produce message

C = consume message

::

        github hook BuildRequest
            |
            |HTTP
            V
        Travis Servers
            |
            |P(configTask)
            V
     -----------------------------------------------------------------------------------
    |                                   RabbitMQ                                        |
     -----------------------------------------------------------------------------------
      |               ^              |                |              ^
      |C(configTask)  |P(buildTask)  |C(buildLog)     |C(buildTask)  |P(buildLog)
      V               |              V                V              |
     ---------------------------------------        ------------------------
    |              Travis Hubs              |      |    Travis Workers      |
    |                   |                   |      |          |             |
    |     fetch and parse .travis.yml       |      |          |             |
    |     collect build logs and process    |      |          |             |
    |     deliver notifications(email/IRC)  |      |        build           |
     ---------------------------------------        ------------------------
                   |
            /--------------+
            | build log db |
            +--------------/



