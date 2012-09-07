#!/usr/bin/env python
#encoding=utf-8
'''Demo of Matplotlib usage
'''

import matplotlib.pyplot as plt
import numpy as np
import urllib2
from lxml.html import parse
import re

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
        plt.plot([v-1 for v in x], [v*2 for v in y])
        #plt.savefig('_demo.png')
        plt.show()

    def web_scraping(self, url = "http://it.wikipedia.org/wiki/Demografia_d'Italia"):
        user_agent = 'Mozilla/5.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent': user_agent}

        req = urllib2.Request(url, headers = headers)
        res = urllib2.urlopen(req)
        doc = parse(res).getroot()
        table = doc.cssselect('table.wikitable')[0]

        years, people = [], []
        for row in table.cssselect('tr')[1:-1]:
            data = row.cssselect('td')
            t_years = data[0].text_content()
            t_years = re.sub('\[.*\]', '', t_years)

            t_people = data[1].text_content()
            t_people = t_people.replace('.', '')

            years.append(int(t_years))
            people.append(int(t_people))

        plt.plot(years, people)
        plt.xlabel('year')
        plt.ylabel('people')
        plt.xticks(range(min(years), max(years), 10))
        plt.title('web scraping demo')
        plt.grid()
        plt.show()



if __name__ == '__main__':
    demo = Demo()
    demo.web_scraping()
    demo.simplest()
