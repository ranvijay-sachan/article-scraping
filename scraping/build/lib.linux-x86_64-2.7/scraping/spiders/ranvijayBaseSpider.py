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
import sys,traceback
import csv
import datetime
import time
import string
import urllib2
import urllib
import random
import thread
import unicodedata
from os import listdir
from os.path import isfile, join
from scrapy import log
from scrapy import signals
from scrapy.spider import BaseSpider
from scrapy.exceptions import CloseSpider
from scrapy.http import Request
from scrapy.xlib.pydispatch import dispatcher
from scraping.utils import sendMail
from scraping import settings

class ranvijayBaseSpider(BaseSpider):
    name = "ranvijayBaseSpider"
    download_delay = 0
    rootPath = ""
    inputLocation = ""
    outputLocation = ""
    logLocation = ""
    errorLocation = ""
    outputPath = ""
    errorPath = ""
    startTime = ""
    waitInSecs = 0
    maxOutFileSize = 0
    retryEnabled = 1
    noOfConsecutiveFailures = 0
    noOfAllowedConsecFailures = 0
    numTotalRequests = 0
    # Stores response stats in following order: successful(200), Failed (all others)
    numResponses = [0, 0]
    numDataItems = 0
    outputFlags = 0
    headerArray = []
    failedURLs = []
    parsedData = []
    exitCode = 0
    alertUrl = ""
    metaArray = []
    inputFileName = ""
    toEmail = ""
    headerIndexTitle = ""
    ouputCsvName = ""
    pkID = ""
    brandName = ""

    def __init__(self, rootPath=None, waitInSecs=0, maxOutFileSize=0, retryEnabled=1, outColumns=None, meta=None, numConsecFailures=0, alertUrl=None, name=None, inputFileName=None, toEmail=None, headerIndexTitle=None, ouputCsvName=None, pkID=None, inputLocation=None, outputLocation=None, logLocation=None, errorLocation=None, brandName=None, **kwargs):
	if name is not None:
		self.name = name
	super(ranvijayBaseSpider, self).__init__(self.name, **kwargs)

        self.download_delay=float(waitInSecs)

	LOG_FILE = rootPath + "/"+logLocation+"/" + "%s_%s.log" % (self.name, int(time.time()))
        log.log.defaultObserver = log.log.DefaultObserver()
        log.log.defaultObserver.start()
        log.started = False
        log.start(LOG_FILE, loglevel=log.DEBUG)

	if(meta is not None):
		self.metaArray = [x.strip() for x in meta.split(',') if x.strip() != ""]

    	self.headerArray.append("Request URL")
	#for x in self.metaArray:
		#self.headerArray.append(x)

	for idx, columnId in enumerate(self.MASTER_COLUMN_ID):
		if((outColumns is None) or (string.find(outColumns, columnId)>=0) or ((self.multiMatchProcessing == "row") and (self.multiMatchRowColumnIndex == idx))):
			self.outputFlags = 1
			thisHeader = self.MASTER_COLUMN_NAME[idx]
			if((self.multiMatchProcessing == "column") and (self.multiMatchColumnCount[idx] > 1)):
				for i in range(self.multiMatchColumnCount[idx]):
					self.headerArray.append(thisHeader + " " + str(i+1))
			else:
				self.headerArray.append(thisHeader)
		else:
			self.outputFlags = 0

	self.startTime = str(datetime.datetime.now())
	if(rootPath.endswith("/")):
		rootPath = rootPath[0:-1]
    	self.rootPath = rootPath
        self.outputLocation = outputLocation
        self.errorLocation = errorLocation
        self.inputLocation = rootPath + "/"+inputLocation+"/"
    	self.outputPath = rootPath + "/"+outputLocation+"/"
    	self.errorPath = rootPath + "/"+errorLocation+"/"
    	self.waitInSecs = float(waitInSecs)
    	self.maxOutFileSize = maxOutFileSize
    	self.retryEnabled = retryEnabled
    	self.noOfAllowedConsecFailures = int(numConsecFailures)
    	self.inputFileName = inputFileName
        self.ouputCsvName = ouputCsvName
        self.brandName = brandName

 	if pkID is not None:
		self.pkID = pkID
 	if headerIndexTitle is not None:
		self.headerIndexTitle = headerIndexTitle
	if alertUrl is not None:
		self.alertUrl = alertUrl
	if toEmail is not None:
		self.toEmail=[toEmail]
	else:
		self.toEmail=settings.MAIL_TO

    	#self.info("Spider initialized with arguments: RootPath:" + rootPath + ", waitInSecs:" + str(waitInSecs) + ", maxOutFileSize:" + str(maxOutFileSize) + ", retryEnabled:" + str(retryEnabled) + ", outColumns:" + (outColumns if (outColumns is not None) else "ALL") + ", meta:" + str(self.metaArray) + ", numConsecFailures:" + str(numConsecFailures) + ", alertUrl:" + self.alertUrl+", inputFileName: "+inputFileName+", toEmail : "+str(toEmail))
    	dispatcher.connect(self.spider_closed, signal=signals.spider_closed)
    	dispatcher.connect(self.spider_error, signal=signals.spider_error)

    def start_requests(self):
        self.info("inside start request")
    	inputPath = self.inputLocation
    	#inputCSVs = [ f for f in listdir(inputPath) if isfile(join(inputPath, f)) ]
    	inputCSVs = [self.inputFileName]
        self.info("Created By Ranvijay: inputCSVs:" + str(inputCSVs))
        outputCSVs = [self.ouputCsvName]
        self.info("Created By Ranvijay: OutputCSVs:" + str(outputCSVs))

	for thisFile in inputCSVs:
		try:
			self.info("Processing Input CSV: " + join(inputPath, thisFile))
			varCsv = csv.DictReader(open(join(inputPath, thisFile),'rU'), delimiter=',', quotechar='"')

			thisMeta = {"handle_httpstatus_all":1}
			if (self.retryEnabled <= 0):
				thisMeta["dont_retry"] = 1

			for line in varCsv:
				for x in self.metaArray:
					if x in line:
						thisMeta[x] = line[x]
                # line[self.pkID]

				yield Request(self.getformattedCsvHeaderVal(line[self.headerIndexTitle]), dont_filter=True, callback=self.parse_response, meta=thisMeta)
				self.info("after yield requrest")
				self.numTotalRequests = self.numTotalRequests + 1
				#if(self.waitInSecs > 0):
				#time.sleep(int(self.waitInSecs+(round(random.uniform(.1,.9), 1)*self.waitInSecs)))
		except:
			self.error("Unexpected error:")
			self.error(traceback.print_exc())
			self.error("skipping this file because of the above mentioned error...!!!")

    def download_errback(self, response):
        self.info("ranvijay - Download error callback")
        self.info(type(response), repr(response))
        self.info(repr(response.value))
        self.info("error Call back  :       "+ str(type(response), repr(response)))
        self.info("error call back 2    :   "+ str(repr(response.value)))

    def spider_closed(self, spider):
	if len(self.parsedData) != 0:
		self.writeDataCSV()
	if len(self.failedURLs) != 0:
		self.writeErrorCSV()

	bodyExitStatus = " has completed successfully."
	subjectExitStatus = "processing complete"

	if(self.exitCode == 1):
		self.info("going to handle failed requuest from parse response !200:alert url:"+self.alertUrl)
		bodyExitStatus = " has been terminated due to high number of failures.\nThis process will be disabled and needed to enable it manually.\n"
		subjectExitStatus = "processing terminated"
		if(self.alertUrl != ""):
			self.info("going to start new thread")
			thread.start_new_thread(urllib2.urlopen,(urllib2.Request(self.alertUrl),))

	mailBody = "Dear Administrator,\n\n\tThe " + self.name + " scheduled at " + self.startTime + bodyExitStatus + " Following are the detailed statistics:\n\tTotal requests submitted: " + str(self.numTotalRequests) + "\n\tSuccessful requests (response code 200) : " + str(self.numResponses[0]) + "\n\tFailed requests: " + str(self.numResponses[1]) + "\n\tNumber of Output Data Items: " + str(self.numDataItems) + "\n\n Thanks,\n Ranvijay"
	sendMail(self.toEmail, self.name + ": " + subjectExitStatus, mailBody, settings.MAIL_CC)

    def spider_error(self, failure, response, spider):
    	self.info("going to handle failed requuest from spider error::")
    	self.handle_failed_response(response)

    def handle_failed_response(self, response):
    	self.error("Request failed for URL: " + response.url + ", StatusCode: " + str(response.status) + " , noOfAllowedConsecFailures: "+str(self.noOfAllowedConsecFailures) + " ,noOfConsecutiveFailures: "+str(self.noOfConsecutiveFailures))
    	self.failedURLs.append({"url":response.url})
    	self.numResponses[1] = self.numResponses[1] + 1

	self.noOfConsecutiveFailures = self.noOfConsecutiveFailures + 1
	if((self.noOfAllowedConsecFailures > 0) and (self.noOfConsecutiveFailures > self.noOfAllowedConsecFailures)):
		self.exitCode = 1
		raise CloseSpider("Number of consecutive failures exceeded allowed limit")

    def writeDataCSV(self):
        outputCSVName = self.outputPath + self.ouputCsvName
    	outFile = open(outputCSVName, "wt")
    	writer = csv.DictWriter(outFile, fieldnames = self.headerArray)

        headers = {}
        for headerName in self.headerArray:
            headers[headerName] = headerName
        writer.writerow(headers)

    	writer.writerows(self.parsedData)
        outFile.close()

    def writeErrorCSV(self):
    	errorCSVName = self.errorPath + "%s_err_%s.csv" % (self.name, int(time.time()))
    	errFile = open(errorCSVName, "wt")
    	writer = csv.DictWriter(errFile, fieldnames = ["url"])

    	writer.writerow({"url":"url"})
    	writer.writerows(self.failedURLs)
	errFile.close()

    def info(self, text):
	log.msg(text, level=log.INFO, spider=self)

    def error(self, text):
	log.msg(text, level=log.ERROR, spider=self)

    def debug(self, text):
	log.msg(text, level=log.DEBUG, spider=self)

    @staticmethod
    def to_unicode(text):
	try:
		return text.decode("utf-8").encode("ascii", "xmlcharrefreplace")
	except UnicodeDecodeError:
		return text.decode("ascii", "ignore")

    @staticmethod
    def remove_accent(data):
        return  unicodedata.normalize('NFKD', data).encode('ASCII', 'ignore')
