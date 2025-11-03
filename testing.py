from bs4 import BeautifulSoup
import requests

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
    
    for projects in project_divs:
        # print(projects.text.strip())
        name = projects.find('span', class_='repo')
        programminglanguage = projects.find(attrs = {'itemprop': 'programmingLanguage'})
        if name and programminglanguage:
            print(f'project name: {name.text.strip()}\nprogramming language used: {programminglanguage.text.strip()}\n')

url = "https://github.com/elio1222"
page = requests.get(url)
if page.status_code == 200:
    source = BeautifulSoup(page.text, 'lxml')
    # print(source.prettify())
    get_stuff(source)
    get_projects_made(source)

else:
    print('something went wrong during request')
