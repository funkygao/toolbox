#!/usr/bin/env python
#encoding=utf-8
'''Demo of Matplotlib usage
'''

import matplotlib.pyplot as plt
import numpy as np

class Demo(object):

    def simplest(self):
        x, y = [1, 2, 4, 5], [4, 9, 2, 10]
        plt.plot(x, y)
        plt.ylabel('some numbers')
        plt.ylim(0, 10)
        plt.grid(True)
        plt.show()

        #plt.plot(x, y, 'rs', x, [y**2 for y in x], 'g^')
        plt.plot(x, y, x, [v**2 for v in y], 'g^')
        plt.savefig('_demo.png')
        plt.show()


if __name__ == '__main__':
    demo = Demo()
    demo.simplest()
