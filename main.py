from bs4 import BeautifulSoup

with open('home.html', 'r') as html_file:
    content = html_file.read()

soup = BeautifulSoup(content, 'lxml')
tags = soup.find('h5') # finds the first h5 tag
courses_html_tags = soup.find_all('h5') # finds all the tags with h5
# find() and find_all() are similar to quereySelector and querySelectorAll

# for course in courses_html_tags:
#     print(course)

course_cards = soup.find_all('div', class_='card') # selecting html element with specific class

for courses in course_cards:
    print(courses.p) # can specify element within the object

for courses in course_cards:
    print(courses.h5.text) # gets the textContent from html tag