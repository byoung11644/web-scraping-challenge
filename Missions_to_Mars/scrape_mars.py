from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd

def init_browser():
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars_dict = {}

    main_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(main_url)
    main_html = browser.html
    soup = bs(main_html, 'html.parser')
    results = soup.find_all('li', class_='slide')
    for result in results[0]:
        try:
            news_title = result.find('h3').text
            news_body = result.find('div', class_='article_teaser_body').text
            mars_dict['Headline'] = news_title
            mars_dict['Summary'] = news_body
        except AttributeError as e:
            mars_dict['Headline'] = e
    
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)
    img_html = browser.html
    img_soup = bs(img_html, 'html.parser')
    img_results = img_soup.find_all('li', class_='slide')
    for result in img_results[0]:
        try:
            img_div = result.find_all('div', class_='img')
            img = div.find('img')['src']
            img_link = (f'https://www.jpl.nasa.gov{img}')
            mars_dict['Latest_Pic'] = img_link
        except:
            pass
    
    facts_url = 'https://space-facts.com/mars/'
    facts_tables = pd.read_html(facts_url)
    df = facts_tables[0]
    df.columns = ['Category', 'Stat']
    html_facts = df.to_html()
    mars_dict['Facts_Table'] = html_facts

    hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/b3c7c6c9138f57b4756be9b9c43e3a48_valles_marineris_enhanced.tif_full.jpg"},
    {"title": "Cerberus Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg"},
    {"title": "Schiaparelli Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/3778f7b43bbbc89d6e3cfabb3613ba93_schiaparelli_enhanced.tif_full.jpg"},
    {"title": "Syrtis Major Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/555e6403a6ddd7ba16ddb0e471cadcf7_syrtis_major_enhanced.tif_full.jpg"},
    ]
    mars_dict['Hemisphere_Pics'] = hemisphere_image_urls

    return mars_dict