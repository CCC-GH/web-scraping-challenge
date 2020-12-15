"""
HW12 - Mission to Mars
!pip install selenium
!pip install splinter
!pip install tweepy

"""
from splinter import Browser
from bs4 import BeautifulSoup
path={'executable_path':'/Users/coffm/Downloads/chromedriver.exe'}
page=Browser('chrome', **path, headless=False)

# Web Scraping - Mission to Mars
# Scrape the [NASA Mars page Site](https://mars.nasa.gov/page/) 
# Collect the latest page Title and Paragraph Text. Assign the text to variables that you can reference later.
#url='https://mars.nasa.gov/page/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
url='https://mars.nasa.gov/news/'
page.visit(url)
html=page.html
soup=BeautifulSoup(html, 'html.parser')
news=soup.find('div', class_='list_text')
newsTitle=news.find('div', class_='content_title').text
print(newsTitle)
newsParagraph=news.find('div', class_ ='article_teaser_body').text
print(newsParagraph)

# JPL Mars Space Images - Featured Image
# Visit the url for JPL Featured Space Image (https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
# Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called `featured_image_url`.
# Make sure to find the image url to the full size `.jpg` image.
# Make sure to save a complete url string for this image.
imageURL='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
page.visit(imageURL)
html=page.html
soup=BeautifulSoup(html, 'html.parser')
image = (soup.find_all('div', class_='carousel_items')[0].a.get('data-fancybox-href'))
featured = 'https://www.jpl.nasa.gov'+ image
print(featured)

# Visit the Mars Facts webpage [here](https://space-facts.com/mars/) 
# Use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
# Use Pandas to convert the data to a HTML table string.
import pandas
facts_url='https://space-facts.com/mars/'
page.visit(facts_url)
marsData=pandas.read_html(facts_url)
marsData=pandas.DataFrame(marsData[0])
marsFacts=marsData.to_html(header=False, index=False)
marsFacts=((pandas.read_html(marsFacts))[0]).rename(columns={0: "Attribute", 1: "Value"}).set_index(['Attribute'])
print(marsFacts)

# Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.
# You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
# Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys `img_url` and `title`.
# Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.
hemispheresURL='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
page.visit(hemispheresURL)
html=page.html
soup=BeautifulSoup(html, 'html.parser')
marsHemisphere=[]
products=soup.find('div', class_='result-list' )
hemispheres=products.find_all('div', class_='item')
for hemisphere in hemispheres:
    title=hemisphere.find('h3').text
    title=title.replace('Enhanced', '')
    endURL=hemisphere.find('a')['href']
    imageURL='https://astrogeology.usgs.gov/' + endURL   
    page.visit(imageURL)
    html=page.html
    soup=BeautifulSoup(html, 'html.parser')
    downloads=soup.find('div', class_='downloads')
    imageURL=downloads.find('a')['href']
    marsHemisphere.append({'title': title, 'img_url': imageURL})
from pprint import pprint
pprint(marsHemisphere)
