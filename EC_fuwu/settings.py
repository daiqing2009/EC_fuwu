# -*- coding: utf-8 -*-

# Scrapy settings for EC_fuwu project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'EC_fuwu'

SPIDER_MODULES = ['EC_fuwu.spiders']
NEWSPIDER_MODULE = 'EC_fuwu.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'EC_fuwu (+http://www.yourdomain.com)'
AUTOTHROTTLE_ENABLED = True

DNSCACHE_ENABLED = True

DB_MYSQL = {'drivername': 'mysql+mysqlconnector',
            'username': 'ec_fuwu',
            'password': 'abcd1234',
            'host':     'localhost',
            'database': 'ec_fuwu'}

DB_SQLITE = {'drivername': 'sqlite',
            'database': 'foo.db'}

ITEM_PIPELINES = {
    'EC_fuwu.pipelines.RdbPipeline':300
}

#AJAXCRAWL_ENABLED = True