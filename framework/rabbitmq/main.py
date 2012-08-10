#!/usr/bin/env python
#encoding=utf-8
'''The CLI for demo

How to start RabbitMQ:
    /opt/app/rabbitmq/sbin/rabbitmq-server

'''

import sys
from client import RabbitMqClient as Client
from rpc import Rpc
import cmd

class DemoCmd(cmd.Cmd):
    '''The demo CLI class that utilize cmd package'''

    def __init__(self):
        cmd.Cmd.__init__(self)

        self.prompt='demo> '
        self.intro = 'RabbitMQ 演示，输入"help"查看可用的命令'

        self.demo = Client()

    def do_ls(self, args):
        self.do_help(args)

    def help_exit(self):
        print '退出程序'

    def do_exit(self, line):
        raise SystemExit

    def help_basic_produce(self):
        print '''简单的发送消息
        参数: 发送的条数 [是否持久化 y/N]'''

    def do_basic_produce(self, args):
        params = args.split()
        num = int(params[0])
        persistant = False
        if len(params) > 1:
            persistant = bool(params[1])
        self.demo.basic_produce(num, persistant)

    def help_fanout_produce(self):
        print '''broadcast的发送消息
        参数: 发送的条数 [是否持久化 y/N]'''

    def do_fanout_produce(self, args):
        params = args.split()
        num = int(params[0])
        persistant = False
        if len(params) > 1:
            persistant = bool(params[1])
        self.demo.basic_produce(num, persistant, 'mac.fanout')

    def help_basic_consume(self):
        print '''接收所有的消息
        参数：[是否ack y/N]'''

    def do_basic_consume(self, args):
        ack = False
        if args=='y':
            ack = True

        self.demo.basic_consume(not ack)

    def help_fanout_consume(self):
        print '''broadcast的消息接收
        参数：[是否ack y/N]'''

    def do_fanout_consume(self, args):
        ack = False
        if args=='y':
            ack = True

        self.demo.fanout_consume(not ack)

    def help_rpc_server_start(self):
        print '''启动rpc server
        无参数'''

    def do_rpc_server_start(self, args):
        rpc = Rpc()
        rpc.start_server()

    def help_rpc_call(self):
        print "rpc_call n -> fib(n)"

    def do_rpc_call(self, args):
        rpc = Rpc()
        ret = rpc.call_rpc(int(args))

if __name__=='__main__':
    demo = DemoCmd()
    demo.cmdloop()
