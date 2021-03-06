# Python News Scraper 
from bs4 import BeautifulSoup
import requests
import re
import smtplib, ssl


limit = 250

port = 465
password = '' # Sender gmail Account password
context = ssl.create_default_context()
sender = '' # Sender gmail account address (hello@gmail.com)
receiver = '' # Email address of recipient
name = 'John'

page = requests.get('https://news.ycombinator.com/')
soup = BeautifulSoup(page.text, 'html.parser')
scores = soup.find_all('span', class_='score')
ids = []
for i in scores:
    points = int(''.join(re.findall(r'[\d]', i.string)))
    if points >= limit:
        ids.append(int(''.join(re.findall(r'[\d]', i.get('id')))))

links = []
titles = []
for i in ids:
    link = soup.find('tr',id=i).find('a', class_='storylink').get('href')
    links.append(link)
    title = soup.find('tr',id=i).find('a', class_='storylink').string
    titles.append(title)

print(links)
print(titles)
message = f"""From: News Collection <from@fromdomain.com>
To: {name} <to@todomain.com>
Subject: Your Hacker News Collection


"""
for count, i in enumerate(titles):
    mess = i + ':   ' + links[count]+'\n\n'
    message += mess
print(message)
with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(sender, password)
    server.sendmail(sender, receiver, message)
