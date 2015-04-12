# article-scraping
A standard base spider structure to use with any kind of spider. we are scraping articles using python scrapy framework.

Scraping Tools Setup on Ubuntu
Reference Environment:
•	Ubuntu 14.04.1 LTS
•	Python 2.7.6
•	OpenSSL 1.0.1f
•	Twistd 13.2.0

Pre-requisites:
•	Python 2.7: Check by running command "python --version". Install if missing.
•	OpenSSL: Check by running command "openssl version". Install if missing.
•	Twisted Framework: Check by running “twistd --version”. Install if missing.

Scrapy Installation:
1.	Run “sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 627220E7”
2.	Run “echo 'deb http://archive.scrapy.org/ubuntu scrapy main' | sudo tee /etc/apt/sources.list.d/scrapy.list”
3.	Run “sudo apt-get update && sudo apt-get install scrapy-0.24”. When asked, enter “Y” to installed extra required packages.
4.	Confirm that Scrapy is installed successfully by running “scrapy version”.

Scrapylib Installation (Master lib required for using Crawlera):
1.	Download zip from “https://github.com/scrapinghub/scrapylib” and unzip to a local folder.
2.	cd to that folder and run “python setup.py install”.

Scrapyd Installation:
1.	Run “apt-get install scrapyd”.
2.	Once finished, check whether “scrapyd” process is running or not. If running, kill the process (force kill if required).
3.	Run “sudo twistd -ny /etc/scrapyd/scrapyd.tac > /var/log/scrapyd/scrapyd.log 2>&1 &”. Confirm that “twistd” process is running.
4.	Go to http://SERVER-IP:6800 to confirm that Scrapyd web console is displayed.


Note: if you found any issue. Please check attached file and permission.

Run curl:
step 1: check services if scrapyd running then kill scrapyd.
Step 2: sudo twistd -ny /etc/scrapyd/scrapyd.tac > /var/log/scrapyd/scrapyd.log 2>&1 &
check server : http://localhost:6800/ 
step 3: run curl in sequence.
I. cd /article-scraping/scraping 
II. curl  http://localhost:6800/schedule.json -d project=scraping -d spider=basePaging
III. Go through the url :  http://localhost:6800/ 
and check job running or not. Do not run second curl until first job not finished.
IV. when first job finished check csv creted or not if creted run second curl.
V. curl  http://localhost:6800/schedule.json -d project=scraping -d spider=rookiestewArticleUrlSpider (when second job finished check csv creted or not if creted run third curl.)
VI. curl  http://localhost:6800/schedule.json -d project=scraping -d spider=rookiestewDetailSpider
VII. For mail set your id and password

