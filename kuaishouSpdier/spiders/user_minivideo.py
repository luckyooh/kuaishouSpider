import json
import re
import logging
import scrapy
import os
import sys

from scrapy.http.request import Request

from kuaishouSpdier.spiders.base import BaseModule
from kuaishouSpdier.common.conf import get_cookie_url
from kuaishouSpdier.common.conf import base_url
from kuaishouSpdier.common.conf import upload_msg_url
from kuaishouSpdier.items import MiniVideoItem
from kuaishouSpdier.common.utils import get_users
from JFB.utils import timestamp_to_localtime
from JFB.utils import timestamp_to_datetime
from kuaishouSpdier.settings import log_file_path

base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

logger = logging.getLogger(__name__)

class UserMinivideoSpider(scrapy.Spider):
    name = 'user_minivideo'

    custom_settings = {
        "DOWNLOAD_DELAY": 0,
        "CONCURRENT_REQUESTS": 50,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 50,
        "CONCURRENT_REQUESTS_PER_IP": 50,
        "LOG_LEVEL": "DEBUG",
        "LOG_FILE": log_file_path.replace("name", name)
    }

    def start_requests(self):
        """遍历账户，先获取cookie"""
        users = get_users()
        for user_id in users:
            yield Request(
                url=get_cookie_url,
                dont_filter=True,
                callback=self.parse_cookie,
                meta={"user_id": user_id, "pcursor": "", "searchSessionId": ""}
            )

    def parse_cookie(self, response):
        """解析cookie，请求列表页"""
        post_data = {
            "operationName": "visionProfilePhotoList",
            "query": "query visionProfilePhotoList($pcursor: String, $userId: String, $page: String, $webPageArea: String) {\n  visionProfilePhotoList(pcursor: $pcursor, userId: $userId, page: $page, webPageArea: $webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      type\n      author {\n        id\n        name\n        following\n        headerUrl\n        headerUrls {\n          cdn\n          url\n          __typename\n        }\n        __typename\n      }\n      tags {\n        type\n        name\n        __typename\n      }\n      photo {\n        id\n        duration\n        caption\n        likeCount\n        realLikeCount\n        coverUrl\n        coverUrls {\n          cdn\n          url\n          __typename\n        }\n        photoUrls {\n          cdn\n          url\n          __typename\n        }\n        photoUrl\n        liked\n        timestamp\n        expTag\n        animatedCoverUrl\n        stereoType\n        videoRatio\n        __typename\n      }\n      canAddComment\n      currentPcursor\n      llsid\n      status\n      __typename\n    }\n    hostName\n    pcursor\n    __typename\n  }\n}\n",
            "variables": {
                "userId": response.meta["user_id"],
                "page": "profile",
                "pcursor": "",
            },
        }
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "PostmanRuntime/7.26.8",
            "Cookie": BaseModule.process_extract_cookie(response),
        }
        yield Request(
            method="POST",
            url=base_url,
            body=json.dumps(post_data),
            dont_filter=True,
            callback=self.parse_list,
            headers=headers,
        )

    def parse_list(self, response):
        """解析列表页，获取信息"""
        res_json = response.json()
        info = res_json.get("data", {}).get("visionProfilePhotoList", {})
        feeds = info.get("feeds", {})
        if not feeds:
            return
        for feed in feeds:
            photo = feed.get("photo", {})
            author = feed.get("author", {})
            publish_time = photo.get("timestamp")
            time_flag = BaseModule.get_time_flag(publish_time)
            if not time_flag:
                continue
            miniVideoItem = MiniVideoItem(
                publish_time=timestamp_to_localtime(publish_time),
                mode="1",
                item_id=photo.get("id"),
                title=photo.get("caption"),
                type="3",
                author=author.get("name"),
                user_id=author.get("id"),
                content="",
                source=f"快手#账户#{author.get('name')}",
                old_cont_url=photo.get("coverUrl"),
                duration=int(photo.get("duration"))//1000,
                video_description=photo.get("caption"),
                old_video_url=re.sub('http.*?com', 'http://v2-mg03.kwaicdn.com', photo.get("photoUrl"))
            )
            yield Request(
                url=upload_msg_url,
                method="POST",
                body=json.dumps(dict(miniVideoItem), ensure_ascii=False),
                headers={"Content-Type": "application/json"},
                callback=self.parse_result,
                meta={"item": miniVideoItem},
                dont_filter=True,
            )

    def parse_result(self, response):
        """获取结果"""
        logger.info(response.meta["item"])
        logger.info(response.text)