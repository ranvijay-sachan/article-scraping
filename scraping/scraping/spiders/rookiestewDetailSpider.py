from scraping.spiders.ranvijayBaseSpider import ranvijayBaseSpider

import urllib

class RookiestewDetailSpider(ranvijayBaseSpider):
    name = "RookiestewDetailSpider"

    # @created by Ranvijay"
    # How spider should process the multiple matching columns. Allowed values are "none", "row" and "column"
    multiMatchProcessing = "row"
    # For each column name, number of multiple matches to add as columns, if "column" value is set above
    multiMatchRowColumnIndex = 0

    MASTER_COLUMN_ID = ["title","publisher", "date"]
    MASTER_COLUMN_NAME = ["title","publisher", "date"]

    def parse_response(self, response):
	self.info("in parse response")
	if response.status != 200:
		self.info("going to handle failed requuest from parse response !200::")
		self.handle_failed_response(response)
        if(self.outputFlags == 1):
	    dataRow = {}
	    dataRow["Request URL"] = self.to_unicode(response.url.strip(' \t\n\r'))
	    for tirleStr in response.xpath("//div[@class='post-block ']/header[@class='entry-header']/h1/text()").extract():
		dataRow['title'] = self.remove_accent(tirleStr)
	    for publisher in response.xpath("//div[@class='entry-content']/p[last()-1]/text()").extract():
		dataRow['publisher'] = publisher.encode('utf-8')
	    for date in response.xpath("//footer[@class='entry-meta single-meta clearfix']/div[@class='entry-date updated']/meta/@content").extract():
		dataRow['date'] = date.encode('utf-8')
		self.parsedData.append(dataRow)
	if ((self.maxOutFileSize > 0) and ((int(self.numResponses[0]) % int(self.maxOutFileSize)) == 0)):
		self.writeDataCSV()
		self.parsedData = []

    def __init__(self, rootPath="/home/ranvijay/Downloads/newTechMonkey/scraping/scraping/spiders", waitInSecs=5, maxOutFileSize=0, retryEnabled=0, outColumns=None, meta=None, numConsecFailures=3, alertUrl="http://www.rookiestew.com/", inputFileName='rookiestewUrls.csv', toEmail=None, headerIndexTitle='url', ouputCsvName='rookiestewUrlsDetail.csv', pkID =None, inputLocation="input-output", outputLocation="input-output", logLocation="logs", errorLocation="error", **kwargs):
	super(RookiestewDetailSpider, self).__init__(rootPath, waitInSecs, maxOutFileSize, retryEnabled, outColumns, meta, numConsecFailures, alertUrl, self.name, inputFileName, toEmail, headerIndexTitle, ouputCsvName, pkID, inputLocation, outputLocation, logLocation, errorLocation, **kwargs)

    def isValidResponse(self, response):
        return

    def sanitizeData(self, dataRow):
        return

    def getformattedCsvHeaderVal(self, urlFromCsv):
        newUrlFromCsv = ""
        newUnquoteUrl = urllib.unquote(urlFromCsv)
        if (not newUnquoteUrl.startswith("http://") and not newUnquoteUrl.startswith("https://")):
            newUrlFromCsv = "http://"+newUnquoteUrl
        else:
            newUrlFromCsv = newUnquoteUrl
        return newUrlFromCsv
