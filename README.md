# Web Scraping Challenge

![image](https://user-images.githubusercontent.com/75215001/130673994-1005e613-9372-40d6-ad0e-8f5cb3595026.png)

For this assignment, I built a web application to scrape four different websites for data related to the Mars Mission. This data is displayed in a single HTML page.
I completed the initial scraping in a Jupyter notebook (see mission_to_mars.ipynb) using BeautifulSoup, Pandas, and Splinter. 

First, I scraped the Mars news site (https://redplanetscience.com/) to collect the latest news title and paragraph text. Next, I scraped the featured space image site 
(https://spaceimages-mars.com). I used Splinter to navigate the site and retrieved the image url for the current Featured Mars Image. For the Mars Facts section, I visited the Mars facts webpage (https://galaxyfacts-mars.com) and used Pandas to scrape a table that contained facts about Mars and Earth. Then, I visited the astrogeology site
(https://marshemispheres.com) to obtain images for each of Mars hemispheres and the titles of the images.

After completing this initial scraping, I used MongoDB with Flask to create a single HTML page to display all of the scraped information (the html file is index.html in the templates folder). This involved creating a function called "scrape" that executed the scraping code from above and returned a dictionary with the scraped data. Using Flask, I created a route called '/scrape' that imports a 'scrape_mars.py' script and calls the scrape function. The returned values were then stored in Mongo as a Python dictionary. I 
also created a root route ('/') that queries the Mongo database and passes the Mars data into the html template to display the data. 

photo credit: redplanetscience.com
