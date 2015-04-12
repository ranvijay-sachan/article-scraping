from scraping.spiders.ranvijayBaseSpider import ranvijayBaseSpider

import urllib

class rookiestewArticleUrlSpider(ranvijayBaseSpider):
    name = "rookiestewArticleUrlSpider"

    # How spider should process the multiple matching columns. Allowed values are "none", "row" and "column"
    multiMatchProcessing = "row"
    # For each column name, number of multiple matches to add as columns, if "column" value is set above
    multiMatchRowColumnIndex = 0

    MASTER_COLUMN_ID = ["url"]
    MASTER_COLUMN_NAME = ["url"]

    def parse_response(self, response):
	self.info("in parse response")
	if response.status != 200:
		self.info("going to handle failed requuest from parse response !200::")
		self.handle_failed_response(response)
		dataRow = {}
        if(self.outputFlags == 1):
            for urlPath in response.xpath("//div[@id='blog-entry']/article/div/header/h1"):
                dataRow = {}
                hrefVal = urlPath.xpath("a/@href").extract()[0]
                dataRow['url'] = hrefVal
                dataRow["Request URL"] = self.to_unicode(response.url.strip(' \t\n\r'))
                self.parsedData.append(dataRow)

 	if ((self.maxOutFileSize > 0) and ((int(self.numResponses[0]) % int(self.maxOutFileSize)) == 0)):
		self.writeDataCSV()
		self.parsedData = []
		
    def __init__(self, rootPath="/home/ranvijay/Downloads/newTechMonkey/scraping/scraping/spiders", waitInSecs=5, maxOutFileSize=0, retryEnabled=0, outColumns=None, meta=None, numConsecFailures=3, alertUrl="http://www.rookiestew.com/", inputFileName='rookiestewUrlInputPaging.csv', toEmail=None, headerIndexTitle='url', ouputCsvName='rookiestewUrls.csv', pkID =None, inputLocation="input-output", outputLocation="input-output", logLocation="logs", errorLocation="error", **kwargs):
	super(rookiestewArticleUrlSpider, self).__init__(rootPath, waitInSecs, maxOutFileSize, retryEnabled, outColumns, meta, numConsecFailures, alertUrl, self.name, inputFileName, toEmail, headerIndexTitle, ouputCsvName, pkID, inputLocation, outputLocation, logLocation, errorLocation, **kwargs)

    def isValidResponse(self, response):
	# Not implemented as of now, assuming all URLs passed to this spider are valid profile URLs
	return 1

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

