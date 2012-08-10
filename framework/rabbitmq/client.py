#!/usr/bin/env python
#encoding=utf-8
'''RabbitMQ demo code

We use RabbitMqDemo class to encapsulate all the features of RabbitMQ.

RabbitMQ特性:
    small code: 17k LOC
    support cluster: easy scalability
    support plugins: i,e. more types of exchange
    flow control: 防止P和C的不同步造成的message泛滥
    transaction: publish and ack of several messages atomic
    message ttl
    can work with Pacemaker to provide HA
    a single queue can run up to 30,000 messages per second
    several queues together can achieve much higher throughput

Definitions:
    Exchange - a message routing agent, a stateless routing table
    Queue    - an infinite buffer. it is stateful, ordered, and can be persistent, transient, public or private
    Binding  - a relationship between an exchange and a queue
    Producer - send messages to exchanges with a routing key
    Consume  - it is consume that create queues, which buffer messages for push to consumers

Routing:
    fanout - it's only capable of mindless broadcasting
             it has no routing key
    direct - use string as routing key
             a message goes to the queues whose binding key exactly matches the routing key of the message
             it's legal to bind multiple queues with the same binding key
             it's legal to bind a queue to multiple binding keys
             channel.queue_bind(
                exchange=exchange_name,
                queue=queue_name,
                routing_key='black')
    topic  - use patterns as routing key
             queues can use wildcard chars in binding


'''

__version__ = '1.0'

import time
import pika

class RabbitMqClient(object):
    '''A RabbitMQ demo class'''

    DURABLE_SUFFIX = '_durable'

    def _durable_queue(self, queue):
        ''' -> name of a queue's durable queue name'''
        return queue + RabbitMqClient.DURABLE_SUFFIX

    def __init__(self, host='localhost', queue='hello'):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.ch = self.conn.channel()

        # 声明RabbitMQ支持的4种exchage
        self.ch.exchange_declare(exchange='mac.direct', type='direct')
        self.ch.exchange_declare(exchange='mac.fanout', type='fanout')
        self.ch.exchange_declare(exchange='mac.topic', type='topic')
        self.ch.exchange_declare(exchange='mac.headers', type='headers')

        # 为该队列名称同时创建transient和persistant 2个队列
        self.ch.queue_declare(queue=queue, durable=False)
        self.ch.queue_declare(queue=self._durable_queue(queue), durable=True)


    def close(self):
        self.conn.close()

    def enable_qos(self, prefetch=1):
        '''Tell RabbitMQ not to give more than one message to a worker at a time.
        
        Don't dispatch a new message to a worker until it has processed and acknowledged the previous one. 
        '''
        self.ch.basic_qos(prefetch_count=prefetch)

    def reset_qos(self):
        pass

    def basic_produce(self, count=1, persistant=False, exchange='mac.direct', queue='hello', body='hello world!'):
        '''向exchange发送消息

        对于fanout exchange，如果还没有绑定到它的queue，那么发送到这里的消息都会自动丢弃
        '''
        if persistant:
            props = pika.BasicProperties(
                    delivery_mode = 2, # make message persistent
                    )
            queue = self._durable_queue(queue)
        else:
            props = pika.BasicProperties()

        now = time.time() # profiler
        for i in range(count):
            self.ch.basic_publish(
                    exchange=exchange,
                    routing_key=queue, # routing_key is queue name, in fanout exchange, it's ignored
                    body="[%d] %s" % (i+1, body),
                    properties=props
                    )
        print '[x] Sent', body, count, 'times', 1000 * (time.time() - now)

    def callback(self, ch, method, properties, body):
        '''不ack的consumer callback'''
        print ch, method, properties, body

    def callback_ack(self, ch, method, properties, body):
        '''含ack的consumer callback'''
        print ch, method, properties, body

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def basic_consume(self, no_ack=True, queue='hello', exchange='mac.direct'):
        '''Works by subscribing a callback to a queue'''
        if no_ack:
            callback = self.callback
        else:
            callback = self.callback_ack
            queue = self._durable_queue(queue)

        # 绑定，同一个queue可以绑定多个routing_key
        self.ch.queue_bind(exchange=exchange, queue=queue, routing_key=queue)

        self.ch.basic_consume(callback, queue=queue, no_ack=no_ack)

        # the loop
        self.ch.start_consuming()

    def fanout_consume(self, no_ack=True, exchange='mac.fanout'):
        '''消费广播型消息

        必须在producer发送fanout消息前启动才能接收到消息'''
        if no_ack:
            callback = self.callback
        else:
            callback = self.callback_ack
            queue = self._durable_queue(queue)

        # 随机生成一个新的临时队列，exclusive指定disconnect时自动删除
        tmp_queue = self.ch.queue_declare(exclusive=True)
        tmp_queue_name = tmp_queue.method.queue

        # 把queue与exchange进行绑定
        self.ch.queue_bind(exchange=exchange, queue=tmp_queue_name)

        self.ch.basic_consume(callback, queue=tmp_queue_name, no_ack=no_ack)

        self.ch.start_consuming()

