#!/usr/bin/env python
# coding: utf-8

#dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# Set up Splinter (preparing automatic browser and specifying that it is Chrome)
    # headless = False means that the browser's actions will be displayed
   
#executable_path = {'executable_path': ChromeDriverManager().install()}
#browser = Browser('chrome', **executable_path, headless=False)

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True) 
    return browser

mars_data= {}

#create scrape function to find title and par
def news_scrape():
    browser = init_browser()
# MARS NEWS

    #create variable for Mars news site url
    url = 'https://redplanetscience.com/'

    #visit the url
    browser.visit(url)
    response = browser.html
    
    #create BeautifulSoup object and parse
    soup = bs(response, 'html.parser')
    
    #retrieve title and paragraph from most recent article
    news_title = soup.find('div', class_='content_title').text
    #print(f"title {news_title}")
    mars_data['news_title']=news_title
    
    news_paragraph = soup.find('div', class_='article_teaser_body').text
    mars_data['news_paragraph'] = news_paragraph
    #print(f"paragraph {news_paragraph}")
    
    return (news_title, news_paragraph)
    
    #return mars_data

# MARS SPACE IMAGES - Featured Image

def image_scrape():
    browser = init_browser()
    
    #visit url using Splinter    
    featured_image_url = 'https://spaceimages-mars.com'
    browser.visit(featured_image_url)
    
   
    
    #
    image_element = browser.find_by_tag('button')[1]
    image_element.click()
    #create html object
    html_image = browser.html
    mars_soup = bs(html_image, 'html.parser')
    
    img_url = mars_soup.find('img', class_='fancybox-image').get('src') 
    #print(featured_image_url)
    #print(img_url)
    link = f'{featured_image_url}/{img_url}'
    #print(link)
    #parse html using Beautiful Soup and create one full image url
    
    #print(featured_image_url)    
    return (link)
    
    # return data
    #return mars_data

# MARS FACTS

def mars_facts():
   
    #create variable for Mars facts url

    url = 'https://galaxyfacts-mars.com/'

    #visit the url
    #browser.visit(url)
    #response = browser.html
    
    #read_html looks for table-like elements in the webpage
    #has created index and columns
    mars_df = pd.read_html(url)[0]
    mars_df.columns = ['Description', 'Mars', 'Earth']

    #mars_df = mars_df.set_index('Description')
    #inplace=True means to reflect changes without creating a new variable
    mars_df.set_index('Description', inplace=True)
     
    return(mars_df.to_html())    
   
 
def mars_hemispheres():
    browser = init_browser()
    # scrape images of Mars' hemispheres from astrogeology site
    hemisphere_url = 'https://marshemispheres.com'
    browser.visit(hemisphere_url)
    hemi_list = []
    hemi_dict = {}
    #loop 4 times, see below; look for product item every time during loop
    #index first time will be 0
    #index.click to click on that one browser 
    for index in range(4):
        browser.find_by_css('a.product-item img')[index].click()
        url_text =  browser.html
        hemisphere_soup = bs(url_text, 'html.parser')
        title = hemisphere_soup.find('h2', class_='title').get_text()
        link = hemisphere_soup.find('a', text='Sample').get('href')        
        
        hemi_dict['title'] = title
        hemi_dict['link'] = link
        
        hemi_list.append(hemi_dict)
        #this hits the back button in the browser
        browser.back()
    return(hemi_list) 

  

#this is a function that calls other functions
# calling news_scrape finds title and par
def scrape_all():    
    news_title, news_paragraph = news_scrape()
    featured_image_url = image_scrape()
    mars_facts_html = mars_facts()
    hemi_list = mars_hemispheres()
    
    #use these same keys to retrieve in index html
    mars_data = {
        'news_title': news_title,
        'news_paragraph': news_paragraph,
        'featured_image_url': featured_image_url,
        'mars_facts_html': mars_facts_html,
        'hemi_list': hemi_list
        }
    return(mars_data)
     
if __name__=='__main__':
    scrape_all()

   