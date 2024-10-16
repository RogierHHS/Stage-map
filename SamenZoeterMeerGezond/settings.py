# ## DIT IS EEN SETTING VOOR ALS JE ERRORS KRIJGT MET HET RUNNEN VAN DE SPIDERS
# ## ZORGT ER VOOR DAT JE DE VOLLEDIGE LOGS KUNT ZIEN EN ALLE DEBUG LOGS DIE WE INSTELLEN ZICH OOK DAADWERKELIJK LATEN ZIEN

# # Log level (optional: INFO, DEBUG, WARNING, ERROR)
# LOG_LEVEL = 'DEBUG'  # Of 'INFO' als je minder details wilt

# # Sla de logs op in een bestand
# LOG_FILE = 'scrapy_log.txt'

# # Om de grootte van het bestand te beperken, kun je 'LOG_STDOUT' aanzetten, zodat stdout ook in het logbestand terechtkomt
# LOG_STDOUT = True



# Scrapy settings for zoetermeerwijzer project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "SamenZoeterMeerGezond"

SPIDER_MODULES = ["SamenZoeterMeerGezond.spiders"]
NEWSPIDER_MODULE = "SamenZoeterMeerGezond.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "SamenZoetermeerGezond (+https://samenzoetermeergezond.nl/)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32



# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "zoetermeerwijzer.middlewares.ZoetermeerwijzerSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "zoetermeerwijzer.middlewares.ZoetermeerwijzerDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   "SamenZoeterMeerGezond.pipelines.CleanDataPipeline": 300,
   'SamenZoeterMeerGezond.pipelines.MySQLPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
