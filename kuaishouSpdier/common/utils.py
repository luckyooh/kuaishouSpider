# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:       utils
   Description :
   Author:          jiangfb
   date:            2021-02-25
-------------------------------------------------
   Change Activity:
                    2021-02-25:
-------------------------------------------------
"""
import logging
from datetime import datetime, timedelta

from kuaishouSpdier.common.dbutil import DataBase

__author__ = 'jiangfb'

logger = logging.getLogger(__name__)

def get_user_keywords():
    logger.info("获取搜索账户关键字")
    sql = "SELECT keyword FROM tb_keyword WHERE type=3 and content_type=1 and keyword_status=0;"
    keywords = DataBase().queryall(sql)
    logger.info("搜索账户关键字：" + "|".join(keywords))
    return keywords

def get_search_keywords():
    logger.info("获取搜索内容关键字")
    sql = "	SELECT keyword FROM tb_keyword WHERE type in (1,2,3) and content_type=1 and keyword_status=0 GROUP BY keyword;"
    keywords = DataBase().queryall(sql)
    logger.info("搜索内容关键字：" + "|".join(keywords))
    return keywords

def get_topic_keywords():
    logger.info("获取搜索话题关键字")
    sql = "SELECT keyword FROM tb_keyword WHERE type in (2,3) and content_type=1  and keyword_status=0 GROUP BY keyword;"
    keywords = DataBase().queryall(sql)
    logger.info("搜索话题关键字：" + "|".join(keywords))
    return keywords

def set_account_finish(user_id, content_type='news'):
    if content_type == 'news':
        sql = '''update tb_source_user set status_1 = 1 where source_channel='头条' AND user_status=0 AND user_id='{}';'''.format(
            user_id)
    else:
        raise ValueError
    return DataBase().execute(sql)

def get_users():
    sql = "select user_id from tb_source_user where source_channel='快手'"
    accounts = DataBase().queryall(sql)
    logger.info(f"账户数量：{len(accounts)}")
    return accounts

def get_accounts(deal_type='add', content_type='news'):
    logger.info(f"获取 [{content_type}] [{deal_type}] 账户")
    if deal_type == 'add' and content_type == 'minivideo':
        sql = """SELECT user_id,scrapy_hours,scrapy_nums FROM tb_source_user WHERE source_channel='渠道' AND user_status = 0 AND status_3=0 AND create_time < DATE_FORMAT(SUBDATE(CURDATE(), INTERVAL 1 DAY),'%Y-%m-%d') AND scrapy_days = 0 AND user_id!='-';"""
    elif deal_type == 'all' and content_type == 'minivideo':
        sql = """SELECT user_id,scrapy_days,scrapy_nums FROM
                (
                SELECT user_id,scrapy_days,scrapy_nums FROM tb_source_user WHERE source_channel='渠道' AND user_status = 0 AND status_3=0 AND create_time = DATE_FORMAT(SUBDATE(CURDATE(), INTERVAL 1 DAY),'%Y-%m-%d') AND user_id!='-'
                UNION ALL
                SELECT user_id,scrapy_days,scrapy_nums FROM tb_source_user WHERE source_channel='渠道' AND user_status = 0 AND status_3=0 AND create_time < DATE_FORMAT(SUBDATE(CURDATE(), INTERVAL 1 DAY),'%Y-%m-%d') AND scrapy_days > 0 AND user_id!='-'
                ) a;"""
    elif deal_type == 'add' and content_type == 'video':
        sql = """SELECT user_id,scrapy_hours,scrapy_nums FROM tb_source_user WHERE source_channel='渠道' AND user_status = 0 AND status_2=0 AND create_time < DATE_FORMAT(SUBDATE(CURDATE(), INTERVAL 1 DAY),'%Y-%m-%d') AND scrapy_days = 0 AND user_id!='-';"""
    elif deal_type == 'all' and content_type == 'video':
        sql = """SELECT user_id,scrapy_days,scrapy_nums FROM
                (
                SELECT user_id,scrapy_days,scrapy_nums FROM tb_source_user WHERE source_channel='渠道' AND user_status = 0 AND status_2=0 AND create_time = DATE_FORMAT(SUBDATE(CURDATE(), INTERVAL 1 DAY),'%Y-%m-%d') AND user_id!='-'
                UNION ALL
                SELECT user_id,scrapy_days,scrapy_nums FROM tb_source_user WHERE source_channel='渠道' AND user_status = 0 AND status_2=0 AND create_time < DATE_FORMAT(SUBDATE(CURDATE(), INTERVAL 1 DAY),'%Y-%m-%d') AND scrapy_days > 0 AND user_id!='-'
                ) a;"""
    elif deal_type == 'add' and content_type == 'news':
        sql = """SELECT user_id,scrapy_hours,scrapy_nums FROM tb_source_user WHERE source_channel='头条' AND user_status = 0 AND status_1=0 AND create_time < DATE_FORMAT(SUBDATE(CURDATE(), INTERVAL 1 DAY),'%Y-%m-%d') AND scrapy_days = 0 AND user_id!='-';"""
    elif deal_type == 'all' and content_type == 'news':
        sql = """SELECT user_id,scrapy_days,scrapy_nums FROM
                (
                SELECT user_id,scrapy_days,scrapy_nums FROM tb_source_user WHERE source_channel='头条' AND user_status = 0 AND status_1=0 AND create_time = DATE_FORMAT(SUBDATE(CURDATE(), INTERVAL 1 DAY),'%Y-%m-%d') AND user_id!='-'
                UNION ALL
                SELECT user_id,scrapy_days,scrapy_nums FROM tb_source_user WHERE source_channel='头条' AND user_status = 0 AND status_1=0 AND create_time < DATE_FORMAT(SUBDATE(CURDATE(), INTERVAL 1 DAY),'%Y-%m-%d') AND scrapy_days > 0 AND user_id!='-'
                ) a;"""
    elif deal_type == 'add' and content_type == 'dynamic':
        sql = """SELECT user_id,scrapy_hours,scrapy_nums FROM tb_source_user WHERE source_channel='头条' AND user_status = 0 AND status_4=0 AND create_time < DATE_FORMAT(SUBDATE(CURDATE(), INTERVAL 1 DAY),'%Y-%m-%d') AND scrapy_days = 0 AND user_id!='-';"""
    elif deal_type == 'all' and content_type == 'dynamic':
        sql = """SELECT user_id,scrapy_days,scrapy_nums FROM
                (
                SELECT user_id,scrapy_days,scrapy_nums FROM tb_source_user WHERE source_channel='头条' AND user_status = 0 AND status_4=0 AND create_time = DATE_FORMAT(SUBDATE(CURDATE(), INTERVAL 1 DAY),'%Y-%m-%d') AND user_id!='-'
                UNION ALL
                SELECT user_id,scrapy_days,scrapy_nums FROM tb_source_user WHERE source_channel='头条' AND user_status = 0 AND status_4=0 AND create_time < DATE_FORMAT(SUBDATE(CURDATE(), INTERVAL 1 DAY),'%Y-%m-%d') AND scrapy_days > 0 AND user_id!='-'
                ) a;"""
    else:
        raise ValueError
    accounts = DataBase().queryall(sql)
    logger.info(f"账户数量：{len(accounts)}")
    return accounts


def set_account_init(deal_type='add', content_type='news'):
    logger.info(f"[{content_type}] [{deal_type}] 账户初始化")
    if deal_type == 'add' and content_type == 'minivideo':
        sql = '''update tb_source_user set status_3 = 0 where source_channel='渠道' AND user_status=0 AND create_time < DATE_FORMAT(SUBDATE(CURDATE(), INTERVAL 1 DAY),'%Y-%m-%d') AND scrapy_days = 0;'''
    elif deal_type == 'all' and content_type == 'minivideo':
        sql = '''update tb_source_user set status_3 = 0 where source_channel='渠道' AND user_status=0 AND (create_time = DATE_FORMAT(SUBDATE(CURDATE(), INTERVAL 1 DAY),'%Y-%m-%d')OR(create_time < DATE_FORMAT(SUBDATE(CURDATE(), INTERVAL 1 DAY),'%Y-%m-%d') AND scrapy_days > 0));'''
    elif deal_type == 'add' and content_type == 'video':
        sql = '''update tb_source_user set status_2 = 0 where source_channel='渠道' AND user_status=0 AND create_time < DATE_FORMAT(SUBDATE(CURDATE(), INTERVAL 1 DAY),'%Y-%m-%d') AND scrapy_days = 0;'''
    elif deal_type == 'all' and content_type == 'video':
        sql = '''update tb_source_user set status_2 = 0 where source_channel='渠道' AND user_status=0 AND (create_time = DATE_FORMAT(SUBDATE(CURDATE(), INTERVAL 1 DAY),'%Y-%m-%d')OR(create_time < DATE_FORMAT(SUBDATE(CURDATE(), INTERVAL 1 DAY),'%Y-%m-%d') AND scrapy_days > 0));'''
    elif deal_type == 'add' and content_type == 'news':
        sql = '''update tb_source_user set status_1 = 0 where source_channel='头条' AND user_status=0 AND create_time < DATE_FORMAT(SUBDATE(CURDATE(), INTERVAL 1 DAY),'%Y-%m-%d') AND scrapy_days = 0;'''
    elif deal_type == 'all' and content_type == 'news':
        sql = '''update tb_source_user set status_1 = 0 where source_channel='头条' AND user_status=0 AND (create_time = DATE_FORMAT(SUBDATE(CURDATE(), INTERVAL 1 DAY),'%Y-%m-%d')OR(create_time < DATE_FORMAT(SUBDATE(CURDATE(), INTERVAL 1 DAY),'%Y-%m-%d') AND scrapy_days > 0));'''
    elif deal_type == 'add' and content_type == 'dynamic':
        sql = '''update tb_source_user set status_4 = 0 where source_channel='头条' AND user_status=0 AND create_time < DATE_FORMAT(SUBDATE(CURDATE(), INTERVAL 1 DAY),'%Y-%m-%d') AND scrapy_days = 0;'''
    elif deal_type == 'all' and content_type == 'dynamic':
        sql = '''update tb_source_user set status_4 = 0 where source_channel='头条' AND user_status=0 AND (create_time = DATE_FORMAT(SUBDATE(CURDATE(), INTERVAL 1 DAY),'%Y-%m-%d')OR(create_time < DATE_FORMAT(SUBDATE(CURDATE(), INTERVAL 1 DAY),'%Y-%m-%d') AND scrapy_days > 0));'''

    else:
        raise ValueError
    status = DataBase().execute(sql)
    logger.info(f"账户初始化数量：{status}")
    return status


def set_topic_init(deal_type='add', content_type='video'):
    if deal_type == 'add' and content_type == 'video':
        sql = '''update tb_source_topic set status_3 = 0 where source_channel='头条' AND topic_status=0 AND create_time < DATE_FORMAT(SUBDATE(CURDATE(), INTERVAL 1 DAY),'%Y-%m-%d') AND scrapy_days = 0;'''
    elif deal_type == 'all' and content_type == 'video':
        sql = '''update tb_source_topic set status_3 = 0 where source_channel='头条' AND topic_status=0 AND (create_time = DATE_FORMAT(SUBDATE(CURDATE(), INTERVAL 1 DAY),'%Y-%m-%d')OR(create_time < DATE_FORMAT(SUBDATE(CURDATE(), INTERVAL 1 DAY),'%Y-%m-%d') AND scrapy_days > 0));'''
    elif deal_type == 'add' and content_type == 'news':
        sql = '''update tb_source_topic set status_1 = 0 where source_channel='头条' AND topic_status=0 AND create_time < DATE_FORMAT(SUBDATE(CURDATE(), INTERVAL 1 DAY),'%Y-%m-%d') AND scrapy_days = 0;'''
    elif deal_type == 'all' and content_type == 'news':
        sql = '''update tb_source_topic set status_1 = 0 where source_channel='头条' AND topic_status=0 AND (create_time = DATE_FORMAT(SUBDATE(CURDATE(), INTERVAL 1 DAY),'%Y-%m-%d')OR(create_time < DATE_FORMAT(SUBDATE(CURDATE(), INTERVAL 1 DAY),'%Y-%m-%d') AND scrapy_days > 0));'''

    else:
        raise ValueError
    return DataBase().execute(sql)


def set_topic_finish(topic_id, content_type='news'):
    if content_type == 'video':
        sql = '''update tb_source_topic set status_3 = 1 where source_channel='头条' AND topic_status=0 AND topic_id='{}';'''.format(
            topic_id)
    elif content_type == 'news':
        sql = '''update tb_source_topic set status_1 = 1 where source_channel='头条' AND topic_status=0 AND topic_id='{}';'''.format(
            topic_id)
    else:
        raise ValueError
    return DataBase().execute(sql)


def get_topics(deal_type='all', content_type='video'):
    if deal_type == 'add' and content_type == 'video':
        sql = """SELECT topic_name,scrapy_hours,scrapy_nums FROM tb_source_topic WHERE source_channel='快手' AND topic_status = 0 AND status_3=0 AND create_time < DATE_FORMAT(SUBDATE(CURDATE(), INTERVAL 1 DAY),'%Y-%m-%d') AND scrapy_days = 0 AND topic_name!='-';"""
    elif deal_type == 'all' and content_type == 'video':
        sql = """SELECT topic_name,scrapy_days,scrapy_nums FROM
                (
                SELECT topic_name,scrapy_days,scrapy_nums FROM tb_source_topic WHERE source_channel='头条' AND topic_status = 0 AND status_3=0 AND create_time = DATE_FORMAT(SUBDATE(CURDATE(), INTERVAL 1 DAY),'%Y-%m-%d') AND topic_name!='-'
                UNION ALL
                SELECT topic_name,scrapy_days,scrapy_nums FROM tb_source_topic WHERE source_channel='头条' AND topic_status = 0 AND status_3=0 AND create_time < DATE_FORMAT(SUBDATE(CURDATE(), INTERVAL 1 DAY),'%Y-%m-%d') AND scrapy_days > 0 AND topic_name!='-'
                ) a;"""
    elif deal_type == 'add' and content_type == 'news':
        sql = """SELECT topic_id,topic_name,scrapy_hours,scrapy_nums FROM tb_source_topic WHERE source_channel='头条' AND topic_status = 0 AND status_1=0 AND create_time < DATE_FORMAT(SUBDATE(CURDATE(), INTERVAL 1 DAY),'%Y-%m-%d') AND scrapy_days = 0 AND topic_name!='-';"""
    elif deal_type == 'all' and content_type == 'news':
        sql = """SELECT topic_id,topic_name,scrapy_days,scrapy_nums FROM
                (
                SELECT topic_id,topic_name,scrapy_days,scrapy_nums FROM tb_source_topic WHERE source_channel='头条' AND topic_status = 0 AND status_1=0 AND create_time = DATE_FORMAT(SUBDATE(CURDATE(), INTERVAL 1 DAY),'%Y-%m-%d') AND topic_name!='-'
                UNION ALL
                SELECT topic_id,topic_name,scrapy_days,scrapy_nums FROM tb_source_topic WHERE source_channel='头条' AND topic_status = 0 AND status_1=0 AND create_time < DATE_FORMAT(SUBDATE(CURDATE(), INTERVAL 1 DAY),'%Y-%m-%d') AND scrapy_days > 0 AND topic_name!='-'
                ) a;"""
    else:
        raise ValueError
    return DataBase().queryall(sql)