# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:       common
   Description :
   Author:          jiangfb
   date:            2021-06-23
-------------------------------------------------
   Change Activity:
                    2021-06-23:
-------------------------------------------------
"""
__author__ = 'jiangfb'
from JFB.utils import timestamp_to_datetime
from JFB.utils import get_delta_datetime

class BaseModule:

    @staticmethod
    def process_extract_cookie(response):
        default_cookie = "kpf=PC_WEB; kpn=KUAISHOU_VISION; clientid=3; did=web_bf582010d8de3bb64b6664e5f9f548fb"

        response_cookies = response.headers.getlist("Set-Cookie")
        if response_cookies:
            result_cookies = []
            for cookie in response_cookies:
                result_cookies.append(cookie.decode().split("; ")[0])
            return "; ".join(result_cookies)
        return default_cookie

    @staticmethod
    def get_time_flag(publish_time):
        publish_time_datetime = timestamp_to_datetime(publish_time)
        scrapy_time_datetime = get_delta_datetime(-1)
        if scrapy_time_datetime > publish_time_datetime:
            return False
        return True