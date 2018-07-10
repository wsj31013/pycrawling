import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import sys
import codecs
from datetime import date

# module for send email
import smtplib
from email.mime.text import MIMEText

nowDate = date.today().strftime('%Y-%m-%d')

req = requests.get('http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf')
html = req.text
bsObj = BeautifulSoup(html, 'html.parser')
book_page_urls = []
for a in bsObj.select('div.title a[href^="http://www.kyobobook.co.kr/product/detailViewKor.laf"]'):
    book_page_urls.append(a.attrs.get('href'))


# print(book_page_urls)
with open('result.txt', 'a', encoding='utf-8') as f:
    for book_page_url in book_page_urls:
        req = requests.get(book_page_url)
        bsObj = BeautifulSoup(req.text, 'html.parser')
        title = bsObj.select('h1.title strong')[0].get_text().strip()
        author = bsObj.select('span.name  a')[0].get_text()
        # print (title + " / " + "저자:" + author)
        data = (title + " / " + '저자:' + author + "\n")
        f.write(data)

# send email
gmail_send_user = '보내는 사람 email'
gmail_send_pw = '보내는 사람 email password'
recipients = ['받는 사람 email01', '받는 사람 email02']


def send_email():
    mail_text = codecs.open('./result.txt', 'r', encoding='utf-8')
    msg = MIMEText(mail_text.read())
    mail_text.close()
    msg['Subject'] = nowDate + '_Kyobo Best Seller TOP20'
    msg['From'] = gmail_send_user
    msg['To'] = ', '.join(recipients)

    try:
        gmail_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        gmail_server.login(gmail_send_user, gmail_send_pw)
        gmail_server.sendmail(gmail_send_user, recipients, msg.as_string())
        gmail_server.quit()
        print('success sending email')
    except:
        print('Fail to send email')


if __name__ == "__main__":
    send_email()
