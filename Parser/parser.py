from bs4 import BeautifulSoup
import time
import csv
import pandas as pd
from urllib.error import HTTPError
import requests

def transcripts(symbol):
    data = []
    symbol = symbol.upper()
    url = 'http://nasdaq.com/symbol/' + symbol + '/call-transcripts'
    req = requests.get(url)
    try:
        soup = BeautifulSoup(req.content, 'html.parser')
        s1 = soup.find_all("table", id="quotes_content_left_CalltranscriptsId_CallTranscripts")[0]
        href = ""
        for x in s1.find_all("a"):
            print (x)
            if ("earnings-call-transcript" in x.get('href')):
                href = x.get('href')
                break
        if isinstance(href, str):
            parse_site = 'http://www.nasdaq.com' + href
            print(parse_site)
            parse_req = requests.get(parse_site)
            try:
                parse_soup = BeautifulSoup(parse_req.content, 'html.parser')
                s3 = parse_soup.find('div', id="SAarticle")
                for line in s3.find_all('p'):
                    h = line.text
                    if h == "Presentation":
                        break
                    data.append(h)
            except HTTPError as e:
                print('Error code: ', e.code)
    except HTTPError as e:
        print('Error code:', e.code)
    return data

def prices(symbol):
    url = 'http://nasdaq.com/symbol/' + symbol
    req = requests.get(url)
    incr = True
    try:
        soup = BeautifulSoup(req.content, 'html.parser')
        s1 = soup.find_all("div", id = "qwidget_lastsale")[0].text
        s2 = soup.find_all("div", id = "qwidget_netchange")[0]
        print (s2.get("class"))
        if ("Red" in s2.get("class")[1]):
            incr = False
            s2 = "-" + s2.text
        else:
            s2 = "+" + s2.text
        s3 = soup.find_all("div", id = "qwidget_percent")[0]
        if ("Red" in s3.get("class")[1]):
            incr = False
            s3 = "-" + s3.text
        else:
            s3 = "+" + s3.text
        return ("Last known stock price: " + s1, "Net Rate of Change: " + s2, "Percent Increase/Decrease: " + s3,
                "https://charting.nasdaq.com/ext/charts.dll?2-1-14-0-0-512-03NA000000" + symbol + "-&SF:1|5-BG=FFFFFF-BT=0-HT=395-", incr)
    except HTTPError as e:
        print('Error code:', e.code)

symbol = "Anadarko Petroleum Corporation"
symbol = "%20".join(symbol.split(" "))
url = "https://twitter.com/search?f=news&vertical=default&q=" + symbol + "&src=tyah&lang=en"
print (url)
req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')

