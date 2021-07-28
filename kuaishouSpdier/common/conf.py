# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:       conf
   Description :
   Author:          jiangfb
   date:            2021-06-23
-------------------------------------------------
   Change Activity:
                    2021-06-23:
-------------------------------------------------
"""
__author__ = 'jiangfb'

env = "dev"

base_url = "https://www.kuaishou.com/graphql"

get_cookie_url = "https://www.kuaishou.com/"
register_url = "https://id.kuaishou.com/pass/kuaishou/login/passToken"

if env == "dev":
    proxy_ip_url = "http://192.168.200.145:10101/api/proxy_ip?queue_name=toutiao"
    upload_user_url = "http://192.168.200.144:8099/precheck/batchAddUser"
    upload_msg_url = "http://192.168.200.144:8099/precheck/addPreCheckMsgDealed"
    upload_topic_url = "http://192.168.200.144:8099/precheck/batchAddTopic"
    little_url = "http://10.168.36.151:5000/toutiao/"
    dbconf = {
        'host': '192.168.15.127',
        'port': 3306,
        'user': 'root',
        'password': 'jRoQ#BF%P4IN',
        'db': 'precheck',
        'charset': 'utf8mb4'
    }
elif env == "pro":
    proxy_ip_url = "http://10.20.12.29:10101/api/proxy_ip?queue_name=toutiao"
    upload_user_url = "http://10.20.12.29:8099/precheck/batchAddUser"
    upload_msg_url = "http://10.20.12.80:8099/precheck/addPreCheckMsgDealed"
    upload_topic_url = "http://10.20.12.29:8099/precheck/batchAddTopic"
    little_url = "http://10.22.0.17:5000/toutiao/"
    dbconf = {
        'host': 'mysqlspiderdata.service.yctxy',
        'user': 'precheck_rw',
        'password': 'A=4xxnGb4toXbXnx',
        'database': 'precheck',
        'charset': 'utf8mb4'
    }