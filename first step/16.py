
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
    links = []

    blogs = driver.find_elements_by_tag_name('article')
    # print(len(blogs))
    for blog in blogs:

        i = 1
        postdates = blog.find_elements_by_class_name('items-center')
        for postdate in postdates:
            if i== 1:
                i += 1
                continue
            article_dates.append(postdate.text)

        article_titles.append(blog.find_element_by_tag_name('h1').text)

        links.append(blog.find_element_by_tag_name('a').get_attribute('href'))
        # contents = blog.find_elements_by_tag_name('article')
        # for content in contents:
        #     link = content.find_element_by_tag_name('a').get_attribute('href')
        #     links.append(link)
        #     print(link)

    for i in range(0, len(links)):
        driver.get(links[i])
        # time.sleep(2)
        temp = ''
        divs = driver.find_elements_by_class_name('c-wysiwyg')
        for div in divs:
            temp += div.find_element_by_tag_name('p').text
        article_contents.append(temp)

    # print(len(article_dates))
    # print(len(article_titles))
    # print(len(article_contents))

        # contents = blog.find_elements_by_class_name('mb-6')
        # i = 1
        # for content in contents:
        #     if i == 1:
        #         i += 1
        #         continue
        #     article_contents.append(content.text)

    for i in range(0, len(article_dates)):
        add_csv_row(article_dates[i], article_titles[i], article_contents[i])

driver = setUpChrome()
add_csv_head()

pull_blog('https://www.aiha.org/synergist-blog')

i = 2
while i < 19:
  pull_blog('https://www.aiha.org/synergist-blog/p' + str(i))
  time.sleep(2)
  i += 1

print("done")



