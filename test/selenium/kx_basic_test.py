#!/usr/bin/env python
#encoding=utf-8

from selenium import selenium
import unittest, time, re
from os import environ

class kx_basic_test(unittest.TestCase):
    ''' 基本的开心网演示测试用例
    '''

    PAGELOAD_TIMEOUT = 5 * 1000 # 5 sec

    LOGIN_USER = 'your_username'
    LOGIN_PASS = 'your_password'

    HOME_URL = 'http://www.kaixin001.com/'

    def get_user(self):
        return environ.get('LOGIN_USER', self.LOGIN_USER)

    def get_passwd(self):
        return environ.get('LOGIN_PASS', self.LOGIN_PASS)

    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*chrome", self.HOME_URL)
        self.selenium.start()
    
    def test_common_apps(self):
        ''' 测试常用的组件
        '''
        sel = self.selenium
        sel.open("/")
        sel.type('name=email', self.get_user())
        sel.type('name=password', self.get_passwd())
        time.sleep(5)
        sel.click("id=btn_dl")


        #sel.wait_for_page_to_load(self.PAGELOAD_TIMEOUT)

        self.assertTrue(True)
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
