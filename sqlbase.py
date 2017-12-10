#!/usr/bin/env python
# -*- coding: utf8 -*-

import pymysql


class SqlBase:
    def __init__(self, host, port, user, pwd, db):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.db = db
        self.conn = self.__get_connect()

    def __get_connect(self):
        return pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.pwd,
            db=self.db,
            charset="utf8")
