from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
from bs4 import BeautifulSoup

def wait():
    time.sleep(1)

def loop_through_subjects(sub):
    wait()
    WebDriverWait(driver, 5).until(
    EC.presence_of_all_elements_located((By.ID, 'subject'))
    )
    subject = Select(driver.find_element(By.ID, 'subject'))
    subject.select_by_visible_text(f'{sub}')

    wait()
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, 'view_catalog'))
    )
    input = driver.find_element(By.ID, 'view_catalog')
    input.click()

    wait()
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, 'courseSchedExpandAll'))
    )
    expand = driver.find_element(By.ID, 'courseSchedExpandAll')
    expand.click()

    wait()
    class_titles = driver.find_elements(By.CLASS_NAME, 'accordion')
    summaries = driver.find_elements(By.TAG_NAME, 'table')

    # for title in class_titles:
    #     print(title.text)

    # for summary in summaries:
    #     print(summary.text)

    for title, summary in zip(class_titles, summaries):
        print(f'Course: {title.text}\nTable: {summary.text}\n')

service = Service(executable_path='/Users/eliorocha/Downloads/chromedriver-mac-arm64/chromedriver')
driver = webdriver.Chrome(service=service)

url = 'https://engineering.catholic.edu/academics/courses/course-schedules/index.html'
driver.get(url)

subjects = [
    'Biomedical Engineering',
    'Civil & Environmental Engineer',
    'Computer Science',
    'Data Analytics',
    'Electrical Engineering',
    'Engineering Management: O/C',
    'Engineering, General',
    'Materials Science and Engineering',
    'Physics'
]

wait()
WebDriverWait(driver, 5).until(
    EC.presence_of_all_elements_located((By.ID, 'term'))
)
term = Select(driver.find_element(By.ID, 'term'))
term.select_by_visible_text('Spring 2026')

for subject in subjects:
    loop_through_subjects(subject)


driver.quit()
