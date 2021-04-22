#!/usr/bin/env python
# coding: utf-8

#dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

# Set up Splinter (preparing automatic browser and specifying that it is Chrome)
    # headless = False means that the browser's actions will be displayed
   
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False) 
    return browser

mars_data= {}
#create scrape function
def news_scrape():
    browser = init_browser
# MARS NEWS
    

    #create variable for Mars news site url

    url = 'https://redplanetscience.com/'

    #visit the url
    browser.visit(url)
    response = browser.html
    
    #create BeautifulSoup object and parse
    soup = bs(response, 'html.parser')
    
    #retrieve title and paragraph from most recent article
    news_title = soup.find('div', class_='content_title').find('a').text
    print(f"title {news_title}")
    mars_data['news_title']=news_title
    
    news_par = soup.find('div', class_='article_teaser_body').text
    mars_data['news_par'] = news_par
    print(f"paragraph {news_par}")
    
    return mars_data

# MARS SPACE IMAGES - Featured Image

def image_scrape():
    browser = init_browser()
    
    #visit url using Splinter    
    featured_image_url = 'https://spaceimages-mars.com/image/featured/mars1.jpg'
    browser.visit(featured_image_url)
    
    #create html object
    html_image = browser.html
    mars_soup = bs(html_image, 'html.parser')

    #parse html using Beautiful Soup and create one full image url
    image_soup = mars_soup.find('figure', 'html.parser')
    link = 'https://spaceimages-mars.com'
    featured_image_url = link + image_soup

    mars_data['featured_image_url']=featured_image_url
    print(featured_image_url)    
    
    # return data
    return mars_data


# MARS FACTS

def mars_facts():
   

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
    mars_facts_df = pd.DataFrame({" ": labels,
                               "Values": values})
    
    #set new index
    mars_facts_df.set_index(" ", inplace=True)
    
    #display dataframe
    mars_facts_df
    
    #convert dataframe to html table string
    
    mars_facts_df = mars_facts_df.to_html(header=False)
    mars_data['mars_facts_df']= mars_facts_df
    return mars_data


