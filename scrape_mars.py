'''
Homework-12-Web-Scraping-and-Document-Databases

'''
# Import dependencies 
from splinter import Browser
from bs4 import BeautifulSoup
#Site navigation
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)
# Defining scrape & dictionary
def scrape():
    scrapData = {}
    news = marsNews()
    scrapData['mars_news'] = news[0]
    scrapData['mars_paragraph'] = news[1]
    scrapData['mars_image'] = marsImage()
    scrapData['mars_facts'] = marsFacts()
    scrapData['mars_hemisphere'] = marsHem()
    return scrapData
# NASA Mars News
def marsNews():
    try: 
        newsURL = 'https://mars.nasa.gov/news/'
        browser.visit(newsURL)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        article = soup.find('div', class_='list_text')
        newsTitle = article.find('div', class_='content_title').text
        newsParagraph = article.find('div', class_ ='article_teaser_body').text
        news = [newsTitle, newsParagraph]
        return news
    finally:
        browser.quit()
# JPL Mars Space Images - Featured Image
def marsImage():
    try: 
        imageURL = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(imageURL)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        image = soup.find('img', class_='thumb')['src']
        featured_imageURL = 'https://www.jpl.nasa.gov' + image
        return featured_imageURL
    finally:
        browser.quit()
# Mars Facts
def marsFacts():
    try: 
        import pandas as pd
        facts_url = 'https://space-facts.com/mars/'
        browser.visit(facts_url)
        marsData = pd.read_html(facts_url)
        marsData = pd.DataFrame(marsData[0])
        marsData.columns = ['Description', 'Value']
        marsData = marsData.set_index('Description')
        mars_facts = marsData.to_html(index = True, header =True)
        return mars_facts
    finally:
        browser.quit()
# Mars Hemispheres
def marsHem():
    try: 
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        mars_hemisphere = []
        products = soup.find('div', class_ = 'result-list' )
        hemispheres = products.find_all('div', class_='item')
        for hemisphere in hemispheres:
            title = hemisphere.find('h3').text
            title = title.replace('Enhanced', '')
            end_link = hemisphere.find('a')['href']
            image_link = 'https://astrogeology.usgs.gov/' + end_link    
            browser.visit(image_link)
            html = browser.html
            soup=BeautifulSoup(html, 'html.parser')
            downloads = soup.find('div', class_='downloads')
            imageURL = downloads.find('a')['href']
            dictionary = {'title': title, 'img_url': imageURL}
            mars_hemisphere.append(dictionary)
        return mars_hemisphere
    finally:
        browser.quit()