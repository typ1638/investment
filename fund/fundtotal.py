#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import sys
import fundconfig

sys.path.append("..")
from sqlbase import SqlBase

reload(sys)
sys.setdefaultencoding('utf-8')


# url = "http://stock.finance.qq.com/fund/jzzx/kfs.js?0.6718136266059089"


class FundTotal:
    def __init__(self):
        self.fund_total = SqlBase(fundconfig.INVESTMENT_HOST, fundconfig.INVESTMENT_PORT, fundconfig.INVESTMENT_USER,
                                  fundconfig.INVESTMENT_PASSWD, fundconfig.INVESTMENT_DB)

    @staticmethod
    def get_all_fund():
        session = requests.session()
        response = session.get(fundconfig.url_fund_all, headers=fundconfig.headers)
        content = response.content.split('=')[1].split(';')[0]
        return content

    def is_fund_exist(self, fund):
        cursor = self.fund_total.conn.cursor()
        try:
            sql = "SELECT EXISTS( SELECT 1 FROM fund_total WHERE fund_id = '" + fund['fund_id'] + "')"
            cursor.execute(sql)
            self.fund_total.conn.commit()
            return cursor.fetchone()[0]
        finally:
            cursor.close()

    def insert_fund(self, fund):
        cursor = self.fund_total.conn.cursor()
        try:
            sql = "INSERT INTO fund_total (fund_id, fund_name, net_asset_value, up_down, growth_rate, acc_net_value, " \
                  "fund_date, apply, redeem, manager) VALUES (%(fund_id)s, %(fund_name)s, %(net_asset_value)s, " \
                  "%(up_down)s, %(growth_rate)s, %(acc_net_value)s, %(fund_date)s, %(apply)s, %(redeem)s, %(manager)s) "
            value = {'fund_id': fund['fund_id'], 'fund_name': fund['fund_name'],
                     'net_asset_value': fund['net_asset_value'],
                     'up_down': fund['up_down'], 'growth_rate': fund['growth_rate'],
                     'acc_net_value': fund['acc_net_value'],
                     'fund_date': fund['fund_date'], 'apply': fund['apply'], 'redeem': fund['redeem'],
                     'manager': fund['manager']}
            cursor.execute(sql, value)
            self.fund_total.conn.commit()
        finally:
            cursor.close()

    def update_fund(self, fund):
        cursor = self.fund_total.conn.cursor()
        try:
            sql = "UPDATE fund_total SET fund_name=%(fund_name)s, net_asset_value=%(net_asset_value)s, " \
                  "up_down=%(up_down)s, growth_rate=%(growth_rate)s, acc_net_value=%(acc_net_value)s, " \
                  "fund_date=%(fund_date)s, apply=%(apply)s, redeem=%(redeem)s, manager=%(manager)s " \
                  "WHERE fund_id=%(fund_id)s"
            value = {'fund_id': fund['fund_id'], 'fund_name': fund['fund_name'],
                     'net_asset_value': fund['net_asset_value'], 'up_down': fund['up_down'],
                     'growth_rate': fund['growth_rate'], 'acc_net_value': fund['acc_net_value'],
                     'fund_date': fund['fund_date'], 'apply': fund['apply'], 'redeem': fund['redeem'],
                     'manager': fund['manager']}
            cursor.execute(sql, value)
            self.fund_total.conn.commit()
        finally:
            cursor.close()

    def sort_all_fund(self):
        contents = self.get_all_fund().replace('],[', '];[').split(';')
        for content in contents:
            fund = {}
            result = content.replace('[', '').replace(']', '')
            result = result.decode('gbk').encode('utf8')
            print result
            result = result.split(',')
            fund['fund_id'] = result[0].replace('"', '')
            fund['fund_name'] = result[1].replace('"', '')
            fund['net_asset_value'] = float(result[2].replace('"', ''))
            fund['up_down'] = float(result[3].replace('"', ''))
            fund['growth_rate'] = float(result[4].replace('"', ''))
            fund['acc_net_value'] = float(result[5].replace('"', ''))
            fund['fund_date'] = fundconfig.str_to_date(result[6].replace('"', ''))
            fund['apply'] = result[7].replace('"', '')
            fund['redeem'] = result[8].replace('"', '')
            fund['manager'] = result[9].replace('"', '')
            # print fund
            ret = self.is_fund_exist(fund)
            if ret != 1:
                self.insert_fund(fund)
            else:
                self.update_fund(fund)
