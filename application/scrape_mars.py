{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Dependencies\n",
    "from splinter import Browser\n",
    "from bs4 import BeautifulSoup\n",
    "import pandas as  pd\n",
    "import requests\n",
    "import time\n",
    "from webdriver_manager.chrome import ChromeDriverManager"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Executable path to driver\n",
    "def init_browser():\n",
    "    executable_path = {\"executable_path': chromedriver.exe\"}\n",
    "    return Browser(\"chrome\", **executable_path, headless=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [],
   "source": [
    "def scrape ():\n",
    "    browser = init_browser()\n",
    "    mars_data = {}\n",
    "\n",
    "\n",
    "    url = 'https://redplanetscience.com/'\n",
    "    browser.visit(url)\n",
    "    time.sleep(1)\n",
    "    nasa_html = browser.html\n",
    "    nasa_soup = BeautifulSoup(nasa_html, 'html.parser')\n",
    "\n",
    "\n",
    "    news_list = nasa_soup.find('ul', class_='item_list')\n",
    "    first_item = news_list.find('li', class_='slide')\n",
    "    nasa_headline = first_item.find('div', class_='content_title').text\n",
    "    nasa_teaser = first_item.find('div', class_='article_teaser_body').text\n",
    "    mars_data[\"nasa_headline\"] = nasa_headline\n",
    "    mars_data[\"nasa_teaser\"] = nasa_teaser"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# JPL Mars Space Images"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#visit Mars featured space image site via Splinter\n",
    "featured_image_url = 'https://spaceimages-mars.com/image/featured/mars1.jpg'\n",
    "browser.visit(featured_image_url)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#create html object\n",
    "html_image = browser.html\n",
    "main_url = 'https://spaceimages-mars.com'\n",
    "#parse html using Beautiful Soup\n",
    "soup = BeautifulSoup(html_image, 'html.parser')\n",
    "\n",
    "featured_image_url = main_url + featured_image_url\n",
    "#display link to featured image\n",
    "featured_image_url"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Mars Facts"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#visit Mars Facts webpage and scrape table containing facts about the planet\n",
    "mars_facts_url = 'https://galaxyfacts-mars.com'\n",
    "\n",
    "browser.visit(mars_facts_url)\n",
    "#time.sleep(1)\n",
    "mars_facts_html = browser.html\n",
    "mars_facts_soup = BeautifulSoup(mars_facts_html, 'html.parser')\n",
    "\n",
    "fact_table = mars_facts_soup.find('table', class_='table table-striped')\n",
    "column1 = fact_table.find_all('td', class_='column-1')\n",
    "column2 = fact_table.find_all('td', class_='column-2')\n",
    "\n",
    "facets = []\n",
    "values = []\n",
    "\n",
    "for row in column1:\n",
    "    facet = row.text.strip()\n",
    "    facets.append(facet)\n",
    "    \n",
    "for row in column2:\n",
    "    value = row.text.strip()\n",
    "    values.append(value)\n",
    "    \n",
    "mars_facts = pd.DataFrame({\n",
    "    \"Description\":facets,\n",
    "    \"Value\":values\n",
    "    })\n",
    "\n",
    "mars_facts_html = mars_facts.to_html(header=False, index=False)\n",
    "mars_facts\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Mars Hemispheres"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# scrape images of Mars' hemispheres from astrogeology site\n",
    "mars_hemisphere_url = 'https://marshemispheres.com'\n",
    "hemi_dicts = []\n",
    "\n",
    "for i in range(1,9,2):\n",
    "    hemi_dict = {}\n",
    "    \n",
    "    browser.visit(mars_hemisphere_url)\n",
    "    time.sleep(1)\n",
    "    hemispheres_html = browser.html\n",
    "    hemispheres_soup = BeautifulSoup(hemispheres_html, 'html.parser')\n",
    "    hemi_name_links = hemispheres_soup.find_all('a', class_='product-item')\n",
    "    hemi_name = hemi_name_links[i].text.strip('Enhanced')\n",
    "    \n",
    "    detail_links = browser.find_by_css('a.product-item')\n",
    "    detail_links[i].click()\n",
    "    time.sleep(1)\n",
    "    browser.find_link_by_text('Sample').first.click()\n",
    "    time.sleep(1)\n",
    "    browser.windows.current = browser.windows[-1]\n",
    "    hemi_img_html = browser.html\n",
    "    browser.windows.current = browser.windows[0]\n",
    "    browser.windows[-1].close()\n",
    "    \n",
    "    hemi_img_soup = BeautifulSoup(hemi_img_html, 'html.parser')\n",
    "    hemi_img_path = hemi_img_soup.find('img')['src']\n",
    "\n",
    "    print(hemi_name)\n",
    "    hemi_dict['title'] = hemi_name.strip()\n",
    "    \n",
    "    print(hemi_img_path)\n",
    "    hemi_dict['img_url'] = hemi_img_path\n",
    "\n",
    "    hemi_dicts.append(hemi_dict)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.9"
  },
  "varInspector": {
   "cols": {
    "lenName": 16,
    "lenType": 16,
    "lenVar": 40
   },
   "kernels_config": {
    "python": {
     "delete_cmd_postfix": "",
     "delete_cmd_prefix": "del ",
     "library": "var_list.py",
     "varRefreshCmd": "print(var_dic_list())"
    },
    "r": {
     "delete_cmd_postfix": ") ",
     "delete_cmd_prefix": "rm(",
     "library": "var_list.r",
     "varRefreshCmd": "cat(var_dic_list()) "
    }
   },
   "types_to_exclude": [
    "module",
    "function",
    "builtin_function_or_method",
    "instance",
    "_Feature"
   ],
   "window_display": false
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
