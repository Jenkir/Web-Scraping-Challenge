#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as  pd
import requests
import time
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False) 
    return browser

#create dictionary to return scraped data
mars_data= {}
#create scrape function
def scrape():
    
    
#Executable path to driver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


# ## NASA Mars News

# In[3]:


#visit Mars news site via Splinter module
url = 'https://redplanetscience.com/'
browser.visit(url)


# In[4]:


#create html object
html = browser.html

#parse HTML using Beautiful Soup
news_soup = BeautifulSoup(html, 'html.parser')


# In[5]:


news_soup


# In[6]:


news_soup.find('div', class_='content_title').text


# In[7]:


#scrape site and collect latest news title and paragraph text
news_title = news_soup.find('div', class_='content_title').text
news_par = news_soup.find('div', class_='article_teaser_body').text

#display scraped data
print(news_title)
print(news_par)


# # JPL Mars Space Images

# In[8]:


#visit Mars featured space image site via Splinter
featured_image_url = 'https://spaceimages-mars.com/image/featured/mars1.jpg'
browser.visit(featured_image_url)


# In[9]:


#create html object
html_image = browser.html
main_url = 'https://spaceimages-mars.com'
#parse html using Beautiful Soup
soup = BeautifulSoup(html_image, 'html.parser')

featured_image_url = main_url + featured_image_url
#display link to featured image
featured_image_url


# # Mars Facts

# In[10]:


mars_facts_url = 'https://galaxyfacts-mars.com'

#read_html looks for table-like elements in the webpage
#has created index and columns
mars_df = pd.read_html(mars_facts_url)[0]
mars_df.columns = ['Description', 'Mars', 'Earth']

#mars_df = mars_df.set_index('Description')
#inplace=True means to reflect changes without creating a new variable
mars_df.set_index('Description', inplace=True)
mars_df


# In[11]:


mars_df.to_html()


# # Mars Hemispheres

# In[12]:


# scrape images of Mars' hemispheres from astrogeology site
mars_hemisphere_url = 'https://marshemispheres.com'
hemi_dicts = []

for i in range(1,9,2):
    hemi_dict = {}
    
    browser.visit(mars_hemisphere_url)
    time.sleep(1)
    hemispheres_html = browser.html
    hemispheres_soup = BeautifulSoup(hemispheres_html, 'html.parser')
    hemi_name_links = hemispheres_soup.find_all('a', class_='product-item')
    hemi_name = hemi_name_links[i].text.strip('Enhanced')
    
    detail_links = browser.find_by_css('a.product-item')
    detail_links[i].click()
    time.sleep(1)
    browser.find_link_by_text('Sample').first.click()
    time.sleep(1)
    browser.windows.current = browser.windows[-1]
    hemi_img_html = browser.html
    browser.windows.current = browser.windows[0]
    browser.windows[-1].close()
    
    hemi_img_soup = BeautifulSoup(hemi_img_html, 'html.parser')
    hemi_img_path = hemi_img_soup.find('img')['src']

    print(hemi_name)
    hemi_dict['title'] = hemi_name.strip()
    
    print(hemi_img_path)
    hemi_dict['img_url'] = hemi_img_path

    hemi_dicts.append(hemi_dict)

