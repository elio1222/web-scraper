from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def wait():
    time.sleep(1)

def loop_through_subjects(sub, final_term):
    wait()
    lol = 6
    WebDriverWait(driver, lol).until(
    EC.presence_of_all_elements_located((By.ID, "subject"))
    )
    subject = Select(driver.find_element(By.ID, "subject"))
    subject.select_by_visible_text(f"{sub}")

    wait()
    WebDriverWait(driver, lol).until(
        EC.element_to_be_clickable((By.ID, "view_catalog"))
    )
    input = driver.find_element(By.ID, "view_catalog")
    input.click()

    wait()
    WebDriverWait(driver, lol).until(
        EC.element_to_be_clickable((By.ID, "courseSchedExpandAll"))
    )
    expand = driver.find_element(By.ID, "courseSchedExpandAll")
    expand.click()

    wait()
    WebDriverWait(driver, lol).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "coursedescription"))
    )
    description = driver.find_elements(By.CLASS_NAME, "coursedescription")
    for desc in description:
        desc.click()

    wait()
    class_titles = driver.find_elements(By.CLASS_NAME, "accordion")
    summaries = driver.find_elements(By.TAG_NAME, "table")


    # for th_list in sf:
    #     for th in th_list:
    #         print(th.text)

    content = driver.find_elements(By.CLASS_NAME, "morecontent")
    cc = []
    for c in content:
        cc.append(c.find_element(By.TAG_NAME, "span"))

    # for title in class_titles:
    #     print(title.text)

    # for summary in summaries:
    #     print(summary.text)

    # for title, summary, desc in zip(class_titles, summaries, cc):
    #     print(f"Course: {title.text}\nTable: {summary.text}\nContent: {desc.text}\n")

    # for summary in summaries:
    #     x = summary.find_elements(By.TAG_NAME, "th")
    #     table_summary = summary.find_elements(By.TAG_NAME, "td")
    #     for t, data in zip(x, table_summary):
    #         print(f"{t.text} ---> {data.text}")

    # for title, desc in zip(class_titles, cc):
    #     print(f"Course: {title.text}\nContent: {desc.text}\n")

    for title, desc, table in zip(class_titles, cc, summaries):
        string_title = title.text.split()
        code = string_title[0]
        string_title.pop(0)
        rest = " ".join(string_title)
        more = rest.split("(")
        cred = more[1]
        cred = cred[0]
        #print(f"\n===== {code} {rest} =====")
        #print(f"Description: {desc.text}\n")

        rows = table.find_elements(By.TAG_NAME, "tr")

        headers = [h.text for h in rows[0].find_elements(By.TAG_NAME, "th")]  # column names
        cur.execute(
    """
    INSERT INTO COURSE (CRS_CODE, SUBJECT_NAME, TERM, CRS_NAME, CRS_DESC, CRS_CREDIT)
    VALUES (%s, %s, %s, %s, %s, %s);
    """,
    (code, sub, final_term, rest, desc.text, cred)
        )
        # Loop through all section rows except the header row
        course_data = {}
        for row in rows[1:]:
            values = [d.text for d in row.find_elements(By.TAG_NAME, "td")]
            #print(f"VALUESSSSSSSSSS: {values}")
            # Display each section (row)
            #print("\n--- Section ---")
            for h, v in zip(headers, values):
                if h.lower() == "time":
                    parts = v.split("   ")
                    parts = parts[1]
                    new = parts.split()
                    new = "".join(new)
                    #print(f"Time: {new}")
                    course_data[h] = new
                else:
                    #print(f"{h}: {v}")
                    course_data[h] = v

            cur.execute(
    """
    INSERT INTO CLASS (
        CLASS_SECTION_NUMBER, CRS_CODE, CLASS_DAYS, CLASS_TIME,
        CLASS_INSTRUCTOR, CLASS_INSTRUCTION_MODE, CLASS_LOCATION
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (CLASS_SECTION_NUMBER, CRS_CODE) DO NOTHING;
    """,
    (
        course_data.get("Sec"),
        code,
        course_data.get("Day"),
        course_data.get("Time"),
        course_data.get("Instructor"),
        course_data.get("Instruction Mode"),
        course_data.get("Location")
    )
        )




        #print("\n----------------------\n")
        #print(f"{course_data.get("Sec")}, {course_data.get("Day")}, {course_data.get("Time")}, {course_data.get("Instructor")}, {course_data.get("Instruction Mode")}, {course_data.get("Location")}")




service = Service(executable_path="/Users/eliorocha/Downloads/chromedriver-mac-arm64/chromedriver")
# options = Options()
# options.add_argument("--headless=new")
driver = webdriver.Chrome(service=service)#, #options=options)


url = "https://engineering.catholic.edu/academics/courses/course-schedules/index.html"
url2 = "https://arts-sciences.catholic.edu/academics/courses/course-schedules/index.html"
driver.get(url2)

subjects = [
    "Biomedical Engineering",
    "Civil & Environmental Engineer",
    "Computer Science",
    "Data Analytics",
    "Electrical Engineering",
    "Engineering Management: O/C",
    "Engineering, General",
    "Materials Science and Engineering",
    "Physics"
]
first = "Materials Science and Engineering"
second = "Computer Science"
test_subject = [first]

ALL_SUBJECTS = [
    "Accounting",
    "Africana Studies",
    "American Sign Language",
    "Anthropology",
    "Applied Physics & Nanotechnology",
    "Applied Space Weather Research",
    "Arabic",
    "Architecture and Planning",
    "Art",
    "Artificial Intelligence",
    "Biology",
    "Biomedical Engineering",
    "Business",
    "Business Magnet Program Dual Enrollment Course",
    "Canon Law",
    "Chemistry",
    "Chinese",
    "Civil & Environmental Engineer",
    "Classics",
    "College of Arts & Sciences",
    "Computer Science",
    "Dance",
    "Data Analytics",
    "Drama",
    # "Early Christian Studies",
    "Ecclesial Administration and Management",
    "Economics",
    "Education",
    "Electrical Engineering",
    "Engineering Management: O/C",
    "Engineering, General",
    "English",
    "Entrepreneurship",
    "Finance",
    "French",
    "German",
    "Global Studies",
    "Greek",
    "Greek and Latin",
    "History",
    "Honors Sequence Capstone",
    "Honors Sequence Env Studies",
    "Honors Sequence Humanities",
    "Honors Sequence Internship",
    "Honors Sequence Liberal Studies",
    "Honors Sequence Philosophy",
    "Honors Sequence Social Science",
    "Honors Sequence Theology and Religious Studies",
    "Human Rights",
    "Information Systems",
    "Italian",
    "Latin",
    # "Law",
    "Library and Information Science",
    "Management",
    "Marketing",
    "Materials Science and Engineering",
    "Mathematics",
    "Mechanical Engineering",
    "Media & Communication Studies",
    "Medieval and Byzantine Studies",
    "Music",
    "Music Private Instruction",
    "Nursing",
    "Philosophy",
    "Physics",
    "Political Economy",
    "Politics",
    "Psychology",
    "Public Policy",
    "SPS: Administration",
    "SPS: Business",
    "SPS: Computer/Management Information Systems",
    "SPS: Humanities",
    "SPS: Interdisciplinary Studies",
    "SPS: Legal Assisting",
    "SPS: Management (Graduate)",
    "SPS: Management (Undergradaute)",
    "SPS: Philosophy",
    "SPS: Religious Studies",
    "SPS: Social Sciences",
    "Semitics",
    "Social Service",
    "Sociology",
    "Spanish",
    # "Study Abroad - Ntnl University of Ireland Galwway",
    # "Study Abroad - Rose Bruford College",
    # "Study Abroad Institut Catholique de Paris",
    # "Study Abroad Univ de Navarra",
    # "Study Abroad Universidad Pontificia Comillas",
    # "Study Abroad Universitat Abat Oliba",
    # "Study Abroad University of Southampton",
    "Theology and Religious Studies",
    "Undergraduate Studies",
    # "Universidad Panamerica Abroad Program"
]

conn = psycopg2.connect(host="localhost", dbname = "csc363project", user = "postgres", password = os.getenv("password"), port = 5432)

cur = conn.cursor()

wait()
WebDriverWait(driver, 5).until(
    EC.presence_of_all_elements_located((By.ID, "term"))
)
term = Select(driver.find_element(By.ID, "term"))
term.select_by_visible_text("Spring 2026")

final_term = term.first_selected_option.text

# for subject in subjects:
#     loop_through_subjects(subject)
for subject in ALL_SUBJECTS:
    cur.execute("INSERT INTO CATALOG (SUBJECT_NAME, TERM) VALUES(%s, %s);", (subject, final_term))
    loop_through_subjects(subject, final_term)
    conn.commit()

cur.close()
conn.close()

driver.quit()
