# -*- coding: utf-8 -*-

BOT_NAME = 'weibo'

SPIDER_MODULES = ['weibo.spiders']
NEWSPIDER_MODULE = 'weibo.spiders'

ROBOTSTXT_OBEY = False

DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0',
}

# CONCURRENT_REQUESTS 和 DOWNLOAD_DELAY 根据账号池大小调整

CONCURRENT_REQUESTS = 16

DOWNLOAD_DELAY = 1

DOWNLOADER_MIDDLEWARES = {
    'weibo.middlewares.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
    'weibo.middlewares.CookieMiddleware': 300,
    'weibo.middlewares.RedirectMiddleware': 200,
    'weibo.middlewares.IPProxyMiddleware': 100,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 101,
}

ITEM_PIPELINES = {
    'weibo.pipelines.MongoDBPipeline': 300,
}

# MongoDb 配置

LOCAL_MONGO_HOST = '127.0.0.1'
LOCAL_MONGO_PORT = 27017
DB_NAME = 'Sina'

# IP
DOWNLOAD_TIMEOUT = 10

RETRY_TIMES = 15