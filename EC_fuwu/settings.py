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

ITEM_PIPELINES = {
    'EC_fuwu.pipelines.RdbPipeline':300
}

#################Environment Dependent Variables ######################
ENV = 'DEBUG'

#QA machine is linux, use mysqldb instead
QA_DB_MYSQL = {'drivername': 'mysql+mysqldb',
            'username': 'ec_fuwu',
            'password': '{{qa.mysql.password}}',
            'host':     'ec4fuwu2014.mysql.rds.aliyuncs.com',
            'database': 'ec_fuwu'}

#debug in 64bit windows, mysqlconnector is more proper
DEBUG_DB_MYSQL = {'drivername': 'mysql+mysqlconnector',
            'username': 'ec_fuwu',
            'password': 'abcd1234',
            'host':     'localhost',
            'database': 'ec_fuwu'}

DB_SQLITE = {'drivername': 'sqlite',
            'database': 'foo.db'}



#AJAXCRAWL_ENABLED = True