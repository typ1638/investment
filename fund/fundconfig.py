#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
import os

url_base = "http://stock.finance.qq.com/fund/jjgs/80163340.htm"

# 全部基金信息，尾数为随机数，需要从浏览器中获得
url_fund_all = "http://stock.finance.qq.com/fund/jzzx/kfs.js?0.6718136266059089"

# url = 'http://stockjs.finance.qq.com/fundUnitNavAll/data/year_all/000577.js'
# url = 'http://web.ifzq.gtimg.cn/fund/newfund/fundInvesting/getInvesting?app=web&symbol=jj000577&_callback=' \
#       'jQuery111106251916345570652_1511620966309&_=1511620966310'

user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; ' \
             '.NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E; InfoPath.3; Media Center PC 6.0)'
headers = {'User-Agent': user_agent}


INVESTMENT_HOST = '127.0.0.1'
INVESTMENT_PORT = 3306
INVESTMENT_USER = 'root'
INVESTMENT_PASSWD = ''
INVESTMENT_DB = 'investment'


def str_to_date(strdate):
    t = time.strptime(strdate, "%Y-%m-%d")
    y, m, d = t[0:3]
    return datetime.date(y, m, d)


path_base = os.getcwd()
path_pages = path_base + "\\fundpages\\"


special_fund = ['001382', '001520', '001573', '001696']
