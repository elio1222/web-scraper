from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def get_stuff(source):
    print('\nscraping github user page.')
    name = source.find('span', class_='p-name')
    nickname = source.find('span', class_='p-nickname')
    bio = source.find('div', class_='p-note')
    print(f'name: {name.text.strip()}')
    print(f'nickname: {nickname.text.strip()}')
    print(f'bio: {bio.text.strip()}')

def get_projects_made(source):
    print('\nprinting projects user has made on github.')
    project_divs = source.find_all('div', class_ = 'Box')
    print(project_divs)
    if project_divs:
        for projects in project_divs:
            # print(projects.text.strip())
            name = projects.find('span', class_='repo')
            programminglanguage = projects.find(attrs = {'itemprop': 'programmingLanguage'})
            if name and programminglanguage:
                print(f'project name: {name.text.strip()}\nprogramming language used: {programminglanguage.text.strip()}\n')
    else:
        print('user has made NO projects')

url = "https://github.com/elio1222"
page = requests.get(url)

# beautifulsoup stuff
if page.status_code == 200:
    source = BeautifulSoup(page.text, 'lxml')
    # print(source.prettify())
    get_stuff(source)
    get_projects_made(source)

else:
    print('something went wrong during request')

# selenium stuff
url2 = "https://github.com/elio1222?tab=repositories&q=&"
driver = Chrome()
driver.get(url2)
repostring = 'weather-app'

WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.NAME, 'q'))
)
text_box = driver.find_element(By.NAME, 'q')
text_box.send_keys(repostring + Keys.ENTER)

time.sleep(5)

repo = driver.find_element(By.CLASS_NAME, "col-10")
print(repo.text)


time.sleep(3)

driver.quit()

