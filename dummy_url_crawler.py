#!/usr/bin/env python3

# 
# @dave_daves
# dummy URL crawler
# last update: 2019-07-24
# 
# use: python3 dummy_url_crawler.py STARTING_URL

"""
PURPOSE:
Implement a very simple web crawler. 
It should accept a single starting URL, such as https://news.ycombinator.com, as its input. 
It should download the web page available at the input URL and extract the URLs of other pages linked to from the HTML source code. 
Although there are several types of link in HTML, just looking at the href attribute of <a> tags will be sufficient for this task. 
It should then attempt to download each of those URLs in turn to find even more URLs, and then download those, and so on. 
The program should stop after it has discovered 100 unique URLs and print them (one URL per line) as its output.
"""

import sys
import requests
from termcolor import colored, cprint
from bs4 import BeautifulSoup

debug = False

unique_urls = []
max_urls = 100

if len(sys.argv) < 2:
    print("Please provide a starting URL")
    quit()

st_url = sys.argv[1]
print("Starting crawling from URL: " + st_url)


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def get_urls(st_crawl, unique_urls, max, start):
    url = st_crawl
    print("Quering      : " + url + "...")
    r = requests.get(url)
    t = r.text
    #print(t)
    if not debug and "404 Error" in t:
        print('Error.\n')
        quit()
    else:
        soup = BeautifulSoup(t, 'html.parser')
        #soup = BeautifulSoup(html_doc_debug, 'html.parser')

        counter = len(unique_urls)

        for a in soup.find_all("a"):
          if counter < max_urls and a['href'] != st_crawl and a not in unique_urls:
            if not a['href'].startswith("http"):
              href = st_crawl + "/" + a['href']
            else:
              href = a['href']
            counter = counter + 1
            print("New URL found  #" + str(counter).zfill(3) + ": " + href)
            unique_urls.append(href)

        #check found urls
        if len(unique_urls) < max_urls :
          get_urls(unique_urls[start+1], unique_urls, max_urls, start)

       
if __name__ == '__main__':
    try:
        get_urls(st_url, unique_urls, max_urls, 0)
    except KeyboardInterrupt:
        stored_exception=sys.exc_info()


