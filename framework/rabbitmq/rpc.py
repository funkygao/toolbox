#!/usr/bin/env python
#encoding=utf-8
'''利于RabbitMQ实现RPC的客户端和服务端

   producer --> RabbitMQ -->  ----------
                             | consumer |
                             | producer |
                              ----------
                                  |
                                  |
   consumer <-- RabbitMQ <--------
'''

import uuid
import pika
from client import RabbitMqClient

class Rpc(RabbitMqClient):
    '''RPC server & client via RabbitMQ'''

    def start_server(self, queue='rpc_queue'):
        '''可以启动多个server，他们会自动load balance'''
        self.ch.queue_declare(queue=queue)

        self.ch.basic_qos(prefetch_count=1)
        self.ch.basic_consume(self.on_client_request, queue=queue)

        print '[x] Awaiting RPC requsts'
        self.ch.start_consuming()

    def fib(self, n):
        '''A demo server side function implementation'''
        if n in (0, 1):
            return n
        else:
            return self.fib(n-1) + self.fib(n-2)

    def on_client_request(self, ch, method, properties, body):
        '''RPC 服务器处理每个客户端的请求
        it's a callback of rpc queue'''
        n = int(body)
        print "[.] fib(%d)" % n

        # 调用执行函数
        response = self.fib(n)

        # 把执行结果发布给客户端consume的队列
        self.ch.basic_publish(
                exchange='', # 使用默认的direct exchange
                routing_key=properties.reply_to,
                properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                body=str(response)
                )
        self.ch.basic_ack(delivery_tag = method.delivery_tag)

    def on_server_response(self, ch, method, properties, body):
        if self.corr_id == properties.correlation_id:
            self.response = body

    def call_rpc(self, n, queue='rpc_queue'):
        # 创建一个临时的reply_to队列
        result = self.ch.queue_declare(exclusive=True)
        callback_queue = result.method.queue

        # 在此队列上获取服务器发来的计算结果
        self.ch.basic_consume(self.on_server_response, no_ack=True, queue=callback_queue)

        # 把请求通过队列发送给服务器，并指定reply_to队列等参数
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.ch.basic_publish(
                exchange='', # 使用默认的direct exchange
                routing_key=queue,
                properties=pika.BasicProperties(
                    reply_to=callback_queue,
                    correlation_id = self.corr_id,
                    ),
                body=str(n)
                )

        # block till server response arrives
        while self.response is None:
            self.conn.process_data_events()

        r = int(self.response)
        print 'call rpc(%s) returns %s' % (n, r)
        return r

