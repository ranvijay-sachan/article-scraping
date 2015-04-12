BOT_NAME = 'scraping'

SPIDER_MODULES = ['scraping.spiders']
NEWSPIDER_MODULE = 'scraping.spiders'

MAIL_FROM="ranvijay5686@gmail.com"
MAIL_HOST="smtp.gmail.com"
MAIL_PORT=587
MAIL_USER="ranvijay5686@gmail.com"
MAIL_PASS="password"
MAIL_TO = ["ranvijay5686@gmail.com"]
MAIL_CC = ["ranvijay5686@gmail.com"]

DOWNLOADER_MIDDLEWARES = {'scraping.middleware.RandomUserAgentMiddleware': 400,
			  'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
}
DOWNLOAD_TIMEOUT = 1200
CONCURRENT_REQUESTS = 100