# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:       run_kuaishou_search_user
   Description :
   Author:          jiangfb
   date:            2021-06-23
-------------------------------------------------
   Change Activity:
                    2021-06-23:
-------------------------------------------------
"""
__author__ = 'jiangfb'

from scrapy import cmdline

if __name__ == '__main__':
    cmdline.execute(["scrapy", "crawl", "user_minivideo"])