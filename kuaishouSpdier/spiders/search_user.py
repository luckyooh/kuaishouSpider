import json

import scrapy
import logging

from kuaishouSpdier.items import KuaishouItemLoader
from scrapy.http.request import Request

from kuaishouSpdier.spiders.base import BaseModule
from kuaishouSpdier.common.conf import get_cookie_url
from kuaishouSpdier.common.conf import base_url
from kuaishouSpdier.common.conf import upload_user_url
from kuaishouSpdier.common.utils import get_user_keywords
from kuaishouSpdier.settings import log_file_path

from kuaishouSpdier.items import AccountItem

logger = logging.getLogger(__name__)

class SearchUserSpider(scrapy.Spider):
    name = 'search_user'

    custom_settings = {
        "DOWNLOAD_DELAY": 0,
        "CONCURRENT_REQUESTS": 50,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 50,
        "CONCURRENT_REQUESTS_PER_IP": 50,
        "LOG_LEVEL": "DEBUG",
        "LOG_FILE": log_file_path.replace("name", name)
    }

    def start_requests(self):
        keywords = get_user_keywords()
        for keyword in keywords:
            yield Request(
                url=get_cookie_url,
                dont_filter=True,
                callback=self.parse_cookie,
                meta={"keyword": keyword, "pcursor": "", "searchSessionId": ""}
            )

    def parse_cookie(self, response):
        post_data = {
            "operationName": "graphqlSearchUser",
            "query": "query graphqlSearchUser($keyword: String, $pcursor: String, $searchSessionId: String) {\n  visionSearchUser(keyword: $keyword, pcursor: $pcursor, searchSessionId: $searchSessionId) {\n    result\n    users {\n      fansCount\n      photoCount\n      isFollowing\n      user_id\n      headurl\n      user_text\n      user_name\n      verified\n      verifiedDetail {\n        description\n        iconType\n        newVerified\n        musicCompany\n        type\n        __typename\n      }\n      __typename\n    }\n    searchSessionId\n    pcursor\n    __typename\n  }\n}\n",
            "variables": {
                "keyword": response.meta["keyword"],
                "pcursor": response.meta["pcursor"],
                "searchSessionId": response.meta["searchSessionId"],
            },
        }
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "PostmanRuntime/7.26.8",
            "Accept": "application/json",
            "Cookie": BaseModule.process_extract_cookie(response),
        }
        yield Request(
            method="POST",
            url=base_url,
            body=json.dumps(post_data),
            dont_filter=True,
            callback=self.parse_list,
            headers=headers,
            meta={"keyword": response.meta["keyword"]}
        )

    def parse_list(self, response):
        keyword = response.meta["keyword"]
        res_json = response.json()
        info = res_json.get("data", {}).get("visionSearchUser", {})
        users = info.get("users", {})
        if users:
            result_users = []
            for user in users:
                item_loader = KuaishouItemLoader(item=AccountItem(), response=response)

                item_loader.add_value("user_name", user.get("user_name"))
                item_loader.add_value("user_id", user.get("user_id"))
                item_loader.add_value("source_channel", "快手")
                item_loader.add_value("remark", "搜索")
                item_loader.add_value("dept_name", "2")
                item_loader.add_value("search_word", keyword)

                accountItem = item_loader.load_item()

                result_users.append(dict(accountItem))
            yield Request(
                url=upload_user_url,
                method="POST",
                body=json.dumps({"user": result_users}, ensure_ascii=False),
                headers={"Content-Type": "application/json"},
                callback=self.parse_result,
                meta={"item": result_users},
                dont_filter=True,
            )

        pcursor = info.get("pcursor")
        searchSessionId = info.get("searchSessionId")
        if pcursor != "no_more":
            yield Request(
                url=get_cookie_url,
                dont_filter=True,
                callback=self.parse_cookie,
                meta={"keyword": response.meta["keyword"], "pcursor": pcursor, "searchSessionId": searchSessionId}
            )

    def parse_result(self, response):
        logger.info(response.meta["item"])
        logger.info(response.text)