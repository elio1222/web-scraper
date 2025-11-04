from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

service = Service(executable_path='/Users/eliorocha/Downloads/chromedriver-mac-arm64/chromedriver')
driver = webdriver.Chrome(service=service)

# some testing i did, but google shutdown my bot
# url = 'https://google.com'
# driver.get(url)

# WebDriverWait(driver, 5).until(
#     EC.presence_of_element_located((By.CLASS_NAME, "gLFyf"))
# )
# text_box = driver.find_element(By.CLASS_NAME, "gLFyf")
# text_box.send_keys('eliorocha.dev' + Keys.ENTER)

# WebDriverWait(driver, 5).until(
#     EC.presence_of_element_located((By.LINK_TEXT, "Elio's porto"))
# )
# link = driver.find_element(By.LINK_TEXT, "Elio's porto")
# link.click()

# time.sleep(5)
# link_element = driver.find_element(By.XPATH, "//a[@href='youtube.com']") # By href attribute
# link_element.click()

# my portfolio url
url = "https://eliorocha.dev/"
driver.get(url)

# time.sleep(5)

# waits until the hover-links classes are present in page source
WebDriverWait(driver, 5).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, 'hover-links'))
)

# gets the youtube link through XPATH
youtube_link = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'youtube.com')]"))
)

# prints out YOUTUBE LINK
print("YouTube URL:", youtube_link.get_attribute("href"))

# Selenium stores the source HTML in the driver's page_source attribute
page_source = driver.page_source
# page_source loads from driver.page_source

# implementing page_source into bs4, with lxml parser
main = BeautifulSoup(page_source, 'lxml')

# finding elements that match div, with class 'techs-icons
technologies = main.find_all('div', 'techs-icons')
for index, tech in enumerate(technologies):
    print(f'index: {index} tech: {tech.text.strip()}')

# clicks youtube link
# driver.execute_script("arguments[0].scrollIntoView(true);", youtube_link)
# driver.execute_script("arguments[0].click();", youtube_link)


time.sleep(5)

driver.quit()
