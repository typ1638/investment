#!/usr/bin/env python
# -*- coding: utf8 -*-

from fundtotal import FundTotal
from downpage import FundPage
from portfolio import PortFolio

if __name__ == "__main__":
    # 获取全部基金基础数据
    # fund_total = FundTotal()
    # fund_total.sort_all_fund()
    # 下载各个基金页面
    # fund_page = FundPage()
    # fund_page.down_pages()
    # 获取持仓数据
    portfolio = PortFolio()
    portfolio.get_portfolio()
