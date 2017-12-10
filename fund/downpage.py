# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import random
import sys
import fundconfig
import threading
import os

reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append("..")
from sqlbase import SqlBase


class FundPage:
    def __init__(self):
        self.fund_total = SqlBase(fundconfig.INVESTMENT_HOST, fundconfig.INVESTMENT_PORT, fundconfig.INVESTMENT_USER,
                                  fundconfig.INVESTMENT_PASSWD, fundconfig.INVESTMENT_DB)

    @staticmethod
    def down_base(fund_id):
        browser = webdriver.PhantomJS()
        # firefoxProfile = webdriver.FirefoxProfile()
        # firefoxProfile.set_preference('permissions.default.stylesheet', 2)
        # firefoxProfile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
        # firefoxProfile.set_preference('permissions.default.image', 2)
        # browser = webdriver.Firefox(firefoxProfile)
        # locator = (By.CLASS_NAME, "portfolio_content")

        file_name = fundconfig.path_pages + str(fund_id) + ".txt"
        url = "http://gu.qq.com/jj" + fund_id
        browser.get(url)
        time.sleep(1)
        # WebDriverWait(browser, 10, 0.5).until(EC.presence_of_element_located(locator))
        response = browser.page_source
        season_file = open(file_name, 'w')
        season_file.write(response)
        season_file.close()
        print "    " + str(fund_id)
        idle = random.randrange(1, 3, 1)
        time.sleep(idle)
        browser.quit()

    def get_allfund_id(self):
        cursor = self.fund_total.conn.cursor()
        try:
            sql = "SELECT DISTINCT(fund_id) FROM fund_total"
            cursor.execute(sql)
            self.fund_total.conn.commit()
            return cursor.fetchall()
        finally:
            cursor.close()

    def down_pages(self):
        print "fund pages download start"
        allfund_id = self.get_allfund_id()
        fund_num = len(allfund_id)
        obj_num = fund_num / 2
        files = os.listdir(fundconfig.path_pages)
        for i in xrange(fund_num):
            txt = str(allfund_id[i][0]) + '.txt'
            if txt in files:
                print "    " + txt + " exist"
            else:
                self.down_base(allfund_id[i][0])
                # threads = []
                # t1 = threading.Thread(target=self.down_base, args=(allfund_id[i][0],))
                # threads.append(t1)
                # if (i + obj_num) <= fund_num:
                #     t2 = threading.Thread(target=self.down_base, args=(allfund_id[i + obj_num][0],))
                #     threads.append(t2)
                # for t in threads:
                #     t.setDaemon(True)
                #     t.start()
                # t.join()

