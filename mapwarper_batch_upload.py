import glob
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from settings import CHROMEDRIVER_PATH, MAPWARPER_EMAIL, MAPWARPER_PASSWORD, COLLECTIONS

browser = webdriver.Chrome(executable_path = CHROMEDRIVER_PATH)

url = 'http://mapwarper.net/login'

browser.get('http://mapwarper.net/login')

email_input = browser.find_element_by_id('email')
email_input.clear()
email_input.send_keys(MAPWARPER_EMAIL)

password_input = browser.find_element_by_id('password')
password_input.clear()
password_input.send_keys(MAPWARPER_PASSWORD)

browser.find_element_by_xpath('//*[@value="Log in"]').click()

browser.get('http://mapwarper.net/maps/new')

for collection in COLLECTIONS:

    images_path = collection['images_path']
    for image in glob.glob(images_path):
        plat_id = image.rsplit('-', 2)[1]

        title_input = browser.find_element_by_id('map_title')
        title_input.send_keys('Plate {}, {}'.format(plat_id, collection['name']))

        publisher_input = browser.find_element_by_id('map_publisher')
        publisher_input.send_keys(collection['publisher'])

        area_input = browser.find_element_by_id('map_subject_area')
        area_input.send_keys(collection['area'])

        source_input = browser.find_element_by_id('map_source_uri')
        source_input.send_keys(collection['map_source_uri'])
    
        browser.find_element_by_id('map_upload').send_keys(image)

        browser.find_element_by_id('map_submit').click()
        time.sleep(60*2)

        browser.get('http://mapwarper.net/maps/new')
