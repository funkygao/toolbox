#!/bin/env python
#encoding=utf-8
"""
Configuration file is named as [class].conf

fl-run-test test.py
fl-run-bench test.py HttpTest.test_http
fl-build-report --html -o _build/ bench.xml
"""

import unittest
from funkload.FunkLoadTestCase import FunkLoadTestCase

class HttpTest(FunkLoadTestCase):

    def test_http(self):
        SERVER_URL = 'http://localhost'
        PAGES = ('index.html', 'a.php')
        for i in range(10):
            for page in PAGES:
                url = '%s/%s' % (SERVER_URL, page)
                self.get(url, description='Get %s' % url)


if __name__ == '__main__':
    unittest.main()
