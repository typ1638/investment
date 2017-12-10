#!/usr/bin/env python
# -*- coding: utf8 -*-

import fundconfig
from bs4 import BeautifulSoup
import os
import downpage
import datetime

import sys
sys.path.append("..")
from sqlbase import SqlBase


class PortFolio:
    def __init__(self):
        self.fund = SqlBase(fundconfig.INVESTMENT_HOST, fundconfig.INVESTMENT_PORT, fundconfig.INVESTMENT_USER,
                            fundconfig.INVESTMENT_PASSWD, fundconfig.INVESTMENT_DB)

    def is_portfolio_exist(self, portfolio):
        cursor = self.fund.conn.cursor()
        try:
            sql = "SELECT EXISTS( SELECT 1 FROM fund_portfolio WHERE fund_id = '" + portfolio['fund_id'] + \
                  "' AND stock_rank=" + str(portfolio['stock_rank']) + " AND date = '" + str(portfolio['date']) + "')"
            cursor.execute(sql)
            self.fund.conn.commit()
            return cursor.fetchone()[0]
        finally:
            cursor.close()

    def insert_portfolio(self, portfolio):
        cursor = self.fund.conn.cursor()
        try:
            sql = "INSERT INTO fund_portfolio (fund_id, fund_name, fund_type, date, stock_rank, stock_id, stock_name" \
                  ", stock_value, stock_num, stock_rate, stock_url) VALUES (%(fund_id)s, %(fund_name)s, " \
                  "%(fund_type)s, %(date)s, %(stock_rank)s, %(stock_id)s, %(stock_name)s, %(stock_value)s, " \
                  "%(stock_num)s, %(stock_rate)s, %(stock_url)s) "
            value = {'fund_id': portfolio['fund_id'], 'fund_name': portfolio['fund_name'],
                     'fund_type': portfolio['fund_type'], 'date': portfolio['date'],
                     'stock_rank': portfolio['stock_rank'], 'stock_id': portfolio['stock_id'],
                     'stock_name': portfolio['stock_name'], 'stock_value': portfolio['stock_value'],
                     'stock_num': portfolio['stock_num'], 'stock_rate': portfolio['stock_rate'],
                     'stock_url': portfolio['stock_url']}
            cursor.execute(sql, value)
            self.fund.conn.commit()
        finally:
            cursor.close()

    def update_portfolio(self, portfolio):
        cursor = self.fund.conn.cursor()
        try:
            sql = "UPDATE fund_portfolio SET fund_name=%(fund_name)s, fund_type=%(fund_type)s, " \
                  "stock_id=%(stock_id)s, stock_name=%(stock_name)s, stock_value=%(stock_value)s, " \
                  "stock_num=%(stock_num)s, stock_rate=%(stock_rate)s, stock_url=%(stock_url)s " \
                  "WHERE fund_id=%(fund_id)s AND stock_rank=%(stock_rank)s AND date=%(date)s"
            value = {'fund_id': portfolio['fund_id'], 'fund_name': portfolio['fund_name'],
                     'fund_type': portfolio['fund_type'], 'date': portfolio['date'],
                     'stock_rank': portfolio['stock_rank'], 'stock_id': portfolio['stock_id'],
                     'stock_name': portfolio['stock_name'], 'stock_value': portfolio['stock_value'],
                     'stock_num': portfolio['stock_num'], 'stock_rate': portfolio['stock_rate'],
                     'stock_url': portfolio['stock_url']}
            cursor.execute(sql, value)
            self.fund.conn.commit()
        finally:
            cursor.close()

    def get_portfolio(self):
        pages = os.listdir(fundconfig.path_pages)
        for page in pages:
            print page
            fund_id = page.split('.')[0]
            down_num = 0
            page = fundconfig.path_pages + page
            while 1:
                if down_num < 2:
                    fo = open(page, 'r')
                    response = fo.read()
                    fo.close()
                    content = BeautifulSoup(response, 'lxml')
                    exist_1 = content.find(class_='title')
                    exist_2 = content.find(class_='portfolio_content')
                    if (exist_1 is None) or (exist_2 is None):
                        downpage.FundPage.down_base(fund_id)
                        down_num = down_num + 1
                    else:
                        title = content.find(class_='title').find(class_='col_1').get_text()
                        print title
                        if "ETF" in title:
                            break
                        fund_type = content.find(class_='title').find(class_='col_3').get_text()
                        print fund_type
                        if (fund_type != '债券型') and (fund_type != 'QDII'):
                            date = content.find(id='portfolio').find(class_='fr').get_text().split('：')[1]
                            portfolio_content = content.find(class_='portfolio_content').find(class_='col_3')
                            portfolio = {}
                            if portfolio_content:
                                trs = portfolio_content.find_all("tr")
                                for tr in trs:
                                    tds = tr.find_all("td")
                                    if tds:
                                        portfolio['fund_id'] = fund_id
                                        portfolio['fund_name'] = title
                                        portfolio['fund_type'] = fund_type
                                        # portfolio['date'] = datetime.datetime.strptime(date, "%Y-%m-%d")
                                        # print date
                                        portfolio['date'] = date
                                        portfolio['stock_rank'] = int(tds[0].get_text())
                                        portfolio['stock_id'] = tds[1].get_text()
                                        portfolio['stock_name'] = tds[2].get_text()
                                        portfolio['stock_value'] = float(tds[3].get_text().replace('元', ''))
                                        portfolio['stock_num'] = int(float(tds[4].get_text().replace('股', '')))
                                        portfolio['stock_rate'] = float(tds[5].get_text().replace('%', ''))
                                        portfolio['stock_url'] = tds[2].find('a')['href']
                                        ret = self.is_portfolio_exist(portfolio)
                                        if ret != 1:
                                            self.insert_portfolio(portfolio)
                                        else:
                                            self.update_portfolio(portfolio)
                                break
                        else:
                            break
                else:
                    break
