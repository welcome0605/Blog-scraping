
import csv
import sys
import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

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

    blogs = driver.find_elements_by_class_name('type-post')
    # print(len(blogs))
    for blog in blogs:
        postdates = blog.find_elements_by_tag_name('time')
        # article_dates.append(postdates.text)
        for postdate in postdates:
            article_dates.append(postdate.text)

        article_titles.append(blog.find_element_by_tag_name('h2').text)

    for i in range(0, len(article_dates)):
        # print(article_contents[i])
        add_csv_row(article_dates[i], article_titles[i], "")

driver = setUpChrome()
add_csv_head()

i = 2019
while i > 2011:
    j = 12
    while j > 0:
        url = 'https://directorsblog.nih.gov/' + str(i) +'/'
        if i == 2019 and j > 9:
            continue
        if i == 2012 and j == 10:
            break
        url += str(j) + '/'
        print(url)
        # pull_blog(url)
        # sleep(4)
        j -= 1
    time.sleep(5)
    i -= 1

print("done")



