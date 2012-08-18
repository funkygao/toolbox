#!/usr/bin/env python
#encoding=utf-8
'''
使用coroutine实现OS
'''

from Queue import Queue
import time
import select


class SystemCall(object):
    def handle(self): pass


class GetTid(SystemCall):
    def handle(self):
        self.task.sendval = self.task.tid
        self.sched.schedule(self.task)


class NewTask(SystemCall):
    def __init__(self, target):
        self.target = target

    def handle(self):
        tid = self.sched.new(self.target)
        self.task.sendvar = tid
        self.sched.schedule(self.task)


class KillTask(SystemCall):
    def __init__(self, id):
        self.id = id

    def handle(self):
        task = self.sched.get(self.id)
        if task:
            #self.sched.exit(task)
            task.target.close()
            self.task.sendval = True

        self.sched.schedule(self.task)


class Task(object):
    """Task 调度的单位，就是一个coroutine wrapper"""
    id = 0

    def __init__(self, target):
        Task.id += 1
        super(Task, self).__init__()
        self.target = target
        self.tid = Task.id
        self.sendval = None  # value to send

    def __str__(self):
        return "tid:(%d/%d)" % (self.tid, Task.id)

    def run(self):
        return self.target.send(self.sendval)


class Scheduler(object):
    def __init__(self):
        self.ready = Queue()
        self.taskmap = {}
        self.read_waiting = {}
        self.write_waiting = {}

    def new(self, target):
        task = Task(target)
        self.taskmap[task.tid] = task
        self.schedule(task)  # start to schedule
        return task.tid

    def get(self, id):
        return self.taskmap.get(id, None)

    def exit(self, task):
        print "task %d terminated" % task.tid
        raw_input("hit any key to continue")
        del self.taskmap[task.tid]

    def wait_for_read(self, task, fd):
        self.read_waiting[fd] = task

    def wait_for_write(self, task, fd):
        self.write_waiting[fd] = task

    def epoll(self, timeout):
        if self.read_waiting or self.write_waiting:
            r, w, e = select.select(self.read_waiting, self.write_waiting, [], timeout)
            for fd in r:
                self.schedule(self.read_waiting.pop(fd))
            for fd in w:
                self.schedule(self.write_waiting.pop(fd))

    def schedule(self, task):
        self.ready.put(task)

    def _iotask(self):
        while 1:
            if not self.ready:
                self.epoll(None)
            else:
                self.epoll(0)
            yield

    def main_loop(self):
        self.new(self._iotask())

        while self.taskmap:
            task = self.ready.get()
            print '================-task %s-==============' % task
            try:
                result = task.run()
                if isinstance(result, SystemCall):
                    # setup to run the SystemCall on behalf of the task
                    print "setup to run SystemCall", result
                    result.task = task  # current task
                    result.sched = self  # current scheduler
                    result.handle()
                    continue
                self.schedule(task)
            except StopIteration:
                self.exit(task)


def foo():
    for x in range(100):
        yield NewTask(bar())


def bar():
    while 1:
        print "i am bar".upper(), time.strftime("%H:%M:%S")
        yield  # 相当于OS里的trap


def blah():
    while 1:
        tid = yield GetTid()
        print blah.__name__, tid
        yield KillTask(103)


scheduler = Scheduler()
scheduler.new(foo())
scheduler.new(bar())
scheduler.new(blah())
scheduler.main_loop()
