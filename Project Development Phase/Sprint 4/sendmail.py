import configparser
import os
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from sendmail import SendGridAPIClient
from sendgrid.helpers.mail import Mail

config = configparser.ConfigParser()
config.read("config.ini")

def SendmailUsingSendGrid(API,from_email,to_email,subject,html_content):
    if API != None and from_email != None and len(to_email)>0 :
        message = Mail(from_email,to_email,subject,html_content)
        try:
            sg = SendGridAPIClient(API)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)


try:
    settings = config["SETTINGS"]
except:
    settings = {}

API = settings.get("APIKEY",None)
from_email = settings.get("FROM",None)
to_email = settings.get("TO","")

print(API)

subject = "Sample test message"
html_content = "Message Successfully sent through Python Sendgrid"

SendmailUsingSendGrid(API,from_email,to_email,subject,html_content)

