# Scrapy settings for nets project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'nets'

SPIDER_MODULES = ['nets.spiders']
NEWSPIDER_MODULE = 'nets.spiders'
USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)'
RANDOMIZE_DOWNLOAD_DELAY=True

TELNETCONSOLE_ENABLED = False
WEBSERVICE_ENABLED = False
CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 1
#LOG_LEVEL = 'ERROR'
#LOG_FILE = 'data/spider.log'
LOG_STDOUT = False

DOWNLOAD_TIMEOUT=10
RETRY_TIMES = 6
DOWNLOADER_STATS = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'nets (+http://www.yourdomain.com)'

DATABASE = {
    'host':'localhost',
    'user':'movie',
    'passwd':'movie',
    'db':'nets',
    'charset':'utf8'
}
