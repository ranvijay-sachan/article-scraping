from scrapy.mail import MailSender
from scraping import settings

mailer = MailSender(
	smtphost=settings.MAIL_HOST,
	mailfrom=settings.MAIL_FROM,
	smtpuser=settings.MAIL_USER,
	smtppass=settings.MAIL_PASS,
	smtpport=settings.MAIL_PORT)
     
def sendMail(mailto, mailsubject, mailbody, mailcc):
	mailer.send(
		to=mailto, 
		subject=mailsubject, 
		body=mailbody, 
		cc=mailcc)
	