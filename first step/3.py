
import csv
import sys
import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

import requests
from bs4 import BeautifulSoup


import time

output_file = 'blog_data.csv'

def setUpChrome():
    global driver
    # Using Chrome
    chrome_options = webdriver.ChromeOptions()
    #prefs = {"profile.managed_default_content_settings.images": 2}
    #chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    #chrome_options.add_argument('headless')

    scriptpath = os.path.realpath(__file__)
    foldername = os.path.basename(scriptpath)
    scriptpath = scriptpath[:scriptpath.find(foldername)]

    scriptpath += 'chromedriver'

    driver = webdriver.Chrome(scriptpath, chrome_options=chrome_options)
    return driver

def add_csv_head():
    with open(output_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['date', 'title', 'content'])

def add_csv_row(date, title, content):
    with open(output_file, 'a', newline='', encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(
            [date, title, content])

def pull_blog(url):
    driver.get(url)

    article_dates = []
    article_titles = []
    article_contents = []

    blogs = driver.find_elements_by_class_name('post-wrapper')
    for blog in blogs:
        postdates = blog.find_elements_by_tag_name('time')
        for postdate in postdates:
            article_dates.append(postdate.text)

        article_titles.append(blog.find_element_by_tag_name('h2').text)

        contents = blog.find_elements_by_class_name('entry-title')
        for content in contents:
            link = content.find_element_by_tag_name('a').get_attribute('href')
            page = requests.get(link)
            soup = BeautifulSoup(page.content, 'html.parser')
            section = soup.find('section', class_='entry-content') 
            # print(section)
            temp = ''
            for tag in section.find_all('p', 'h3'):
                temp += tag.getText()
            article_contents.append(temp)

    for i in range(0, 10):
        # print(article_titles[i])
        add_csv_row(article_dates[i], article_titles[i], article_contents[i])

driver = setUpChrome()
add_csv_head()

pull_blog('https://www.health.harvard.edu/blog/')

i = 2019
while i > 2008:
  pull_blog('https://www.health.harvard.edu/blog/' + str(i))
  time.sleep(2)
  i -= 1

print("done")



