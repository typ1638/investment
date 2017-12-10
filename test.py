#!/usr/bin/env python
# -*- coding: utf8 -*-

import requests

url = "http://gu.qq.com/jj110005"
user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; ' \
             '.NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E; InfoPath.3; Media Center PC 6.0)'
headers = {'User-Agent': user_agent}


url_1 = "http://web.ifzq.gtimg.cn/fund/newfund/fundInvesting/getInvesting?app=web&symbol=jj110001&_callback=" \
        "jQuery111105335371038042904_1511705232390&_=1511705232391"

url_2 = "http://web.ifzq.gtimg.cn/fund/newfund/fundInvesting/getInvesting?app=web&symbol=jj110005&_callback=" \
        "jQuery1111012463717656336581_1511705139613&_=1511705139614"

session = requests.session()
response = session.get(url, headers=headers)
print response.content
