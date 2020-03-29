from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    # Visit nasa.gov url
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html,"lxml")

    # Get the news title
    news_title = soup.find('div', class_='content_title').text
    
    # Get news text 
    news_p = soup.find('div', class_='article_teaser_body').text


    #vist nasa.gov url 
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, 'lxml')

    # Get featured image
    image_name= soup.find('article', class_='carousel_item')['alt'] 
    base_url = 'https://www.jpl.nasa.gov'
    img_url = soup.find(attrs={'data-title':image_name})["data-fancybox-href"] 
    featured_image_url = base_url + img_url

    # Visit Mars Twitter 
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, 'lxml')

    #Get Mars Weather
    mars_weather= soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    
     #Visit Mars facts url
    url = 'https://space-facts.com/mars/'

    #Get Mars facts table
    tables = pd.read_html(url)
    mars_df = tables[1]
    mars_df.columns = ['Attribute', 'Value']
    html_table = mars_df.to_html(header=None,index=False)
    html_table.replace('\n', '')


  # Visit usgs.gov
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, 'lxml')


    # Empty list to append the dictionaries with title and image url later
    hemisphere_img_urls = []

    #modified x-path to include all 4 hemispheres, using this x-path to aslo get the title at the same time  
    xpath = '//*[@id="product-section"]/div[2]/div/div/a'

    hemisphere_page_anchors = browser.find_by_xpath(xpath)

    # Loop through results 
    for anchor in hemisphere_page_anchors:
        try:
            hemisphere_title = anchor.find_by_tag('h3').text
            hemisphere_href = anchor['href']
            #request the next page using the href
            hemisphere_page = requests.get(hemisphere_href).text
            soup = bs(hemisphere_page, 'lxml')
            anchor_tag_page2 = soup.select('#wide-image > div > ul > li:nth-child(1) > a')
            hemisphere_img_url =  anchor_tag_page2[0]['href']
            img_dict = { "image title": hemisphere_title, "image url": hemisphere_img_url }
            hemisphere_img_urls.append(img_dict)
        except Exception as e:
            print(e)
        
    mars_info = {
        "News_Title": news_title,
        "Paragraph_Text": news_p,
        "Most_Recent_Mars_Image": featured_image_url,
        "Mars_Weather": mars_weather,
        "Mars_Table": html_table,
        "Mars_Hemispheres": hemisphere_img_urls
    }
    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_info