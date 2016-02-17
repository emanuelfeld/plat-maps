import time
from selenium import webdriver
from settings import CHROMEDRIVER_PATH, MAPWARPER_EMAIL, MAPWARPER_PASSWORD, COLLECTIONS
import lxml.html

browser = webdriver.Chrome(executable_path = CHROMEDRIVER_PATH)

# Sign in to Mapwarper

browser.get('http://mapwarper.net/login')

email_input = browser.find_element_by_id('email')
email_input.clear()
email_input.send_keys(MAPWARPER_EMAIL)

password_input = browser.find_element_by_id('password')
password_input.clear()
password_input.send_keys(MAPWARPER_PASSWORD)

browser.find_element_by_xpath('//*[@value="Log in"]').click()

# Get all maps in layer

layer = 'http://mapwarper.net/layers/468'

browser.get(layer)

maps = []
map_urls = []
map_titles = []

def get_map_info():
    source_string = browser.page_source
    root = lxml.html.fromstring(source_string)
    maps.extend(root.xpath('//div[@class="maplist_title"]/a'))
    map_urls.extend([m.attrib['href'] for m in maps])
    map_titles.extend([m.text_content() for m in maps])

while True:
    get_map_info()
    try:
        browser.find_element_by_xpath('//a[@class="next_page"]').click()
    except:
        break

# Download GCPs for each map

for i in range(len(map_urls)):
    browser.get('http://mapwarper.net' + map_urls[i])
    browser.find_element_by_id('aaRectify').click()
    time.sleep(60)
    browser.find_element_by_xpath('//a[@id="controlPointLink"]').click()

    source_string = browser.page_source
    root = lxml.html.fromstring(source_string)

    gcp_table = root.xpath('//table[@id="gcp_table"]/tbody')[0]
    rows = []
    for row in gcp_table.xpath('tr'):
        data = []
        data.append(row.xpath('td[4]/input')[0].value)
        data.append(row.xpath('td[5]/input')[0].value)
        data.append(row.xpath('td[2]/input')[0].value)
        data.append('-' + row.xpath('td[3]/input')[0].value)
        data.append("1")
        rows.append(','.join(data))

    fname = 'plate-' + map_titles[i].split(' ')[1][:-1] + '.points'
    with open('points/{}'.format(fname), 'w') as f:
        f.write('mapX,mapY,pixelX,pixelY,enable\n')
        [f.write('{}\n'.format(row)) for row in rows]
