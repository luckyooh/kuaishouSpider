# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import json
import logging
import random

import requests
from scrapy import signals

from JFB.utils import localtime_to_datetime
from JFB.utils import get_now_datetime

from scrapy.downloadermiddlewares.retry import RetryMiddleware

from kuaishouSpdier.common.conf import proxy_ip_url
from kuaishouSpdier.settings import proxy_pool
from kuaishouSpdier.settings import proxy_num
from kuaishouSpdier.settings import last_proxy

from twisted.internet import defer
from twisted.internet.error import (
    ConnectError,
    ConnectionDone,
    ConnectionLost,
    ConnectionRefusedError,
    DNSLookupError,
    TCPTimedOutError,
    TimeoutError,
)
from twisted.web.client import ResponseFailed
from scrapy.utils.response import response_status_message
from scrapy.core.downloader.handlers.http11 import TunnelError
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

logger = logging.getLogger(__name__)

class MyProxyMiddleware:

    @staticmethod
    def is_expire(proxy_json):
        expire_time_str = proxy_json["data"]["expire_time"]
        expire_time = localtime_to_datetime(expire_time_str)
        now_time = get_now_datetime()
        if expire_time < now_time:
            return True
        return False

    def remove_proxy(self, ip_port, proxy_json):
        res = requests.get(url=proxy_ip_url, data=json.dumps(proxy_json, ensure_ascii=False).encode("utf-8"), timeout=20)
        logger.info(f"delete a ip_port from online: {ip_port}")
        ip_port = self.fill_proxy(res)
        return ip_port

    @staticmethod
    def fill_proxy(res):
        """填充ip池，记录last_proxy"""
        proxy_json = res.json()
        data = proxy_json["data"]
        ip_port = data["ip"] + ":" + str(data["port"])
        proxy_pool[ip_port] = proxy_json
        last_proxy["ip_port"] = ip_port
        last_proxy["proxy_json"] = proxy_json
        logger.info(f"fill in a proxy: {ip_port}, current number of proxies: {len(proxy_pool)}")
        return ip_port

    @staticmethod
    def is_pool_num():
        """判断pool是否大于proxy_num个"""
        num = len(proxy_pool)
        if num >= proxy_num:
            return True
        return False

    @staticmethod
    def in_pool(ip_port):
        """判断是否在池中"""
        if proxy_pool.get(ip_port):
            return True
        return False

    @staticmethod
    def get_random_proxy():
        """从池中随机获取一个代理"""
        ip_port = random.sample(proxy_pool.keys(), 1)[0]
        proxy_json = proxy_pool[ip_port]
        return ip_port, proxy_json

    @staticmethod
    def pack_proxy(ip_port):
        return {
            "http": f"http://{ip_port}",
            "https": f"https://{ip_port}"
        }

    # 判断是否过期：1. 没过期，返回ip_port；2. 过期：删除，封装，返回
    def get_one_proxy(self):
        _is_pool_num = self.is_pool_num()
        if _is_pool_num:
            ip_port, proxy_json = self.get_random_proxy()
            _is_expire = self.is_expire(proxy_json)
            if not _is_expire:
                return self.pack_proxy(ip_port)
            else:
                logger.warning("proxy expire: " + ip_port)
                proxy_pool.pop(ip_port, None)
                ip_port = self.remove_proxy(last_proxy["ip_port"], last_proxy["proxy_json"])
                return self.pack_proxy(ip_port)
        ip_port = self.remove_proxy(last_proxy["ip_port"], last_proxy["proxy_json"])
        return self.pack_proxy(ip_port)

    def process_request(self, request, spider):
        # 数据上传接口不走代理
        if "precheck" in request.url:
            return None
        proxies = self.get_one_proxy()
        if request.url.startswith("https"):
            request.meta['proxy'] = proxies["https"]
        elif request.url.startswith("http"):
            request.meta['proxy'] = proxies["http"]
        else:
            raise Exception("MyProxyMiddleware: 协议错误")
        logger.info("using proxy: {}".format(request.meta['proxy']))
        return None


class MyRetryMiddleware(RetryMiddleware):
    # IOError is raised by the HttpCompression middleware when trying to
    # decompress an empty response
    EXCEPTIONS_TO_RETRY = (defer.TimeoutError, TimeoutError, DNSLookupError,
                           ConnectionDone, ConnectError,
                           ConnectionLost, TCPTimedOutError, ResponseFailed,
                           IOError, TunnelError, ConnectionRefusedError)

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        if "Need captcha" in response.text:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        if (
            isinstance(exception, self.EXCEPTIONS_TO_RETRY)
            and not request.meta.get('dont_retry', False)
        ):
            return self._retry(request, exception, spider)
