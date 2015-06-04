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


