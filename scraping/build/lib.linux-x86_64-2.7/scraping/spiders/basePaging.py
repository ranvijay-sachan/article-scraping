#-------------------------------------------------------------------------------
# Name:        ranvijayBaseSpider
# Purpose:
#
# Author:      Ranvijay
#
# Created:     21/01/2015
# Copyright:   (c) Ranvijay 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from scraping.spiders.ranvijayBaseSpider import ranvijayBaseSpider

import urllib

class basePaging(ranvijayBaseSpider):
    name = "basePaging"
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
        if(self.outputFlags == 1):
            page=None
	    pageCount = response.xpath("//div[@class='pagination']/span[1]/text()").extract()[0].replace('Page 1 of ', '')
	    self.info("page count : "+pageCount)
            if len(pageCount) > 0:
                page = pageCount
		self.info("pageee : "+pageCount)
            if page is not None:
		self.info("111111111111111111")
                for i in range(int(page)):
		    self.info("iiiiiiiiiii"+str(i))
                    dataRow = {}
                    dataRow["Request URL"] = self.to_unicode(response.url.strip(' \t\n\r'))
                    dataRow["url"] = str("http://www.rookiestew.com/page/")+str(i+1)+"/"
		    self.info("loveeeeeeeeeeeeeeeee")
                    self.parsedData.append(dataRow)
            else:
                    dataRow = {}
                    dataRow["Request URL"] = self.to_unicode(response.url.strip(' \t\n\r'))
                    dataRow["url"] = "http://www.rookiestew.com/"
                    self.parsedData.append(dataRow)

     	if ((self.maxOutFileSize > 0) and ((int(self.numResponses[0]) % int(self.maxOutFileSize)) == 0)):
    		self.writeDataCSV()
    		self.parsedData = []


    def __init__(self, rootPath="/home/ranvijay/Downloads/newTechMonkey/scraping/scraping/spiders", waitInSecs=5, maxOutFileSize=0, retryEnabled=0, outColumns=None, meta=None, numConsecFailures=3, alertUrl="http://www.rookiestew.com/", inputFileName='rookiestewUrlInput.csv', toEmail=None, headerIndexTitle='url', ouputCsvName='rookiestewUrlInputPaging.csv', pkID =None, inputLocation="input-output", outputLocation="input-output", logLocation="logs", errorLocation="error", **kwargs):
	super(basePaging, self).__init__(rootPath, waitInSecs, maxOutFileSize, retryEnabled, outColumns, meta, numConsecFailures, alertUrl, self.name, inputFileName, toEmail, headerIndexTitle, ouputCsvName, pkID, inputLocation, outputLocation, logLocation, errorLocation, **kwargs)

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