#!/usr/bin/env python
# coding: utf-8

#dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager


#create scrape function
def scrape():

# MARS NEWS
    # Set up Splinter (preparing automatic browser and specifying that it is Chrome)
    # headless = False means that the browser's actions will be displayed
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #create variable for Mars news site url

    url = 'https://redplanetscience.com/'

    #visit the url
    browser.visit(url)
    response = browser.html
    
    #create BeautifulSoup object and parse
    soup = bs(response, 'html.parser')
    
    #retrieve title and paragraph from most recent article
    news_title = soup.find('div', class_='content_title').text
    news_par = soup.find('div', class_='article_teaser_body').text
   
    return news_title, news_par

# MARS SPACE IMAGES - Featured Image

def featured_image(browser):

    # Set up Splinter browser)
    
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False) 
    
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    
    #code for moving through pages on the website
    time.sleep(5)
    browser.click_link_by_partial_text()
    time.sleep(5)
    browser.click_link_by_partial_text()
    time.sleep(5)
    
    html_image = browser.html
    
    mars_soup = bs(html_image, 'html.parser')

    #parse html using Beautiful Soup
    image_soup = mars_soup.find('figure', 'html.parser')
    link = 'https://spaceimages-mars.com'
    featured_image_url = link + image_soup

    # return data
    
    return featured_image_url


# In[ ]:
# MARS FACTS

def mars_facts():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    #create variable for Mars facts url

    url = 'https://galaxyfacts-mars.com/'

    #visit the url
    browser.visit(url)
    response = browser.html
    
    #create BeautifulSoup object and parse
    facts_soup = bs(response, 'html.parser')
    
    #retrieve table
    table = facts_soup.find('table', 'tablepress tablepress-id-mars')
    
    #retrieve rows in the table
    rows = table.find_all('tr')
    
    #create empty lists to hold td elements from each row (this alternates bt lables and values)
    labels = []
    values = []
    
    #loop through each row; add 1st td element to labels and 2nd to values
    for row in rows:
        td_elements = row.find_all('td')
        labels.append(td_elements[0].text)
        values.append(td_elements[1].text)
   
    #create dataframe to hold table info.
    mars_facts = pd.DataFrame({" ": labels,
                               "Values": values})
    
    #set new index
    mars_facts.set_index(" ", inplace=True)
    
    #display dataframe
    mars_facts
    
    #convert dataframe to html table string
    
    html_table = mars_facts.to_html(header=False)
    return html_table


