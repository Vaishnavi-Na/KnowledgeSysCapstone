from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
import time
from bs4 import BeautifulSoup
import ssl
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
import os


courses_to_scrape=[
  { "subject": "CSE", "course_number": "1110" },
  { "subject": "CSE", "course_number": "1111" },
  { "subject": "CSE", "course_number": "1112" },
  { "subject": "CSE", "course_number": "1113" },
  { "subject": "CSE", "course_number": "1114" },
  { "subject": "CSE", "course_number": "1211" },
  { "subject": "CSE", "course_number": "1213" },
  { "subject": "CSE", "course_number": "1222" },
  { "subject": "CSE", "course_number": "1223" },
  { "subject": "CSE", "course_number": "1224" },
  { "subject": "CSE", "course_number": "2021" },
  { "subject": "CSE", "course_number": "2111" },
  { "subject": "CSE", "course_number": "2112" },
  { "subject": "CSE", "course_number": "2122" },
  { "subject": "CSE", "course_number": "2123" },
  { "subject": "CSE", "course_number": "2133" },
  { "subject": "CSE", "course_number": "2221" },
  { "subject": "CSE", "course_number": "2231" },
  { "subject": "CSE", "course_number": "2321" },
  { "subject": "CSE", "course_number": "2331" },
  { "subject": "CSE", "course_number": "2371" },
  { "subject": "CSE", "course_number": "2421" },
  { "subject": "CSE", "course_number": "2431" },
  { "subject": "CSE", "course_number": "2451" },
  { "subject": "CSE", "course_number": "2501" },
  { "subject": "CSE", "course_number": "3231" },
  { "subject": "CSE", "course_number": "3232" },
  { "subject": "CSE", "course_number": "3241" },
  { "subject": "CSE", "course_number": "3244" },
  { "subject": "CSE", "course_number": "3321" },
  { "subject": "CSE", "course_number": "3341" },
  { "subject": "CSE", "course_number": "3421" },
  { "subject": "CSE", "course_number": "3430" },
  { "subject": "CSE", "course_number": "3461" },
  { "subject": "CSE", "course_number": "3521" },
  { "subject": "CSE", "course_number": "3541" },
  { "subject": "CSE", "course_number": "3901" },
  { "subject": "CSE", "course_number": "3902" },
  { "subject": "CSE", "course_number": "3903" },
  { "subject": "CSE", "course_number": "4191" },
  { "subject": "CSE", "course_number": "4251" },
  { "subject": "CSE", "course_number": "4252" },
  { "subject": "CSE", "course_number": "4253" },
  { "subject": "CSE", "course_number": "4256" },
  { "subject": "CSE", "course_number": "4471" },
  { "subject": "MATH", "course_number": "1151" },
  { "subject": "MATH", "course_number": "1152" },
  { "subject": "MATH", "course_number": "2148" },
  { "subject": "MATH", "course_number": "2174" },
  { "subject": "MATH", "course_number": "2568" },
  { "subject": "MATH", "course_number": "3345" },
  { "subject": "MATH", "course_number": "3346" },
  { "subject": "MATH", "course_number": "3355" },
  { "subject": "MATH", "course_number": "4503" },
  { "subject": "MATH", "course_number": "4504" },
  { "subject": "MATH", "course_number": "4530" },
  { "subject": "MATH", "course_number": "4532" },
  { "subject": "PHYSICS", "course_number": "1250" },
  { "subject": "PHYSICS", "course_number": "1251" },
  { "subject": "PHYSICS", "course_number": "1252" },
  { "subject": "PHYSICS", "course_number": "1281" },
  { "subject": "PHYSICS", "course_number": "1282" },
  { "subject": "PHYSICS", "course_number": "2500" },
  { "subject": "PHYSICS", "course_number": "2501" },
  { "subject": "PHYSICS", "course_number": "2502" },
  { "subject": "ENGR", "course_number": "1181" },
  { "subject": "ENGR", "course_number": "1182" },
  { "subject": "ENGR", "course_number": "1281" },
  { "subject": "ENGR", "course_number": "1282" },
  { "subject": "ENGR", "course_number": "1810" },
  { "subject": "ENGR", "course_number": "1830" },
  { "subject": "ENGR", "course_number": "2120" },
  { "subject": "ENGR", "course_number": "2130" },
  { "subject": "ENGR", "course_number": "2430" },
  { "subject": "ENGR", "course_number": "2530" },
  { "subject": "ENGR", "course_number": "3130" },
  { "subject": "ENGR", "course_number": "4230" },
  { "subject": "ENGR", "course_number": "4231" }
]

semester={
    "6": "AU24",
    "7": "SP25",
    "8": "SU25",
    "9": "AU25"
}

def scrape_page(sem_val,subject, course_number):

    # Select Term
    term_dropdown = Select(driver.find_element(By.ID, "id_term"))
    term_dropdown.select_by_value(sem_val) 

    # Select Subject
    subject_dropdown = Select(driver.find_element(By.ID, "id_subject"))
    subject_dropdown.select_by_value(subject)

    # Enter Course Number
    course_input = driver.find_element(By.ID, "id_number")
    course_input.clear()
    course_input.send_keys(course_number)

    # Click Search button
    search_button = driver.find_element(By.XPATH, "//button[text()='Search']")
    search_button.click()


    try:
        # Wait for the element to be present and visible
        element = WebDriverWait(driver, 1).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".text-xl.font-semibold.mb-4.text-white"))
        )
    except TimeoutException:
        print("Timeout: Element not found.")
        return

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # Extract all result rows
    rows = soup.select("div.grid.grid-cols-7.bg-gray-200")

    # Collect the data
    for row in rows:
        cells = row.find_all("div")
        if len(cells) >= 5:
            time = cells[2].get_text(strip=True)
            room = cells[3].get_text(strip=True)
            instructor = cells[4].get_text(strip=True).replace("\n", " ").strip()
        # Insert into an index called 'courses'
        response = es.index(index="courses", document={
            "subject":subject,
            "term": semester[sem_val],
            "course_number": course_number,
            "time": time,
            "classroom": room,
            "instructor": instructor
        })

# Set up Firefox options
options = Options()
options.add_argument('--headless')  


#Setup elasticsearch through REST API library
ctx = ssl.create_default_context()
ctx.load_verify_locations("http_ca.crt")
ctx.verify_flags &= ~ssl.VERIFY_X509_STRICT
load_dotenv()
es = Elasticsearch('https://localhost:9200', ssl_context=ctx, basic_auth=("elastic", os.getenv('ELASTIC_PASSWORD')))

driver = webdriver.Firefox()

driver.get("https://osucoursesearch.org/")

WebDriverWait(driver, 2)

for course in courses_to_scrape:
    for i in range(6,10,1):
        scrape_page(str(i),course["subject"], course["course_number"])

# Close browser
driver.quit()


