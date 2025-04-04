from bs4 import BeautifulSoup
import re
import json

courses = []
filePath = "GenEd_Webpages/studentChoice.html"
soup = BeautifulSoup(open(filePath, encoding="utf-8"), 'html.parser')
#print(soup.prettify())

divs = soup.find_all("div", class_="col-md-12 light course-info")
#print(divs[0])
for div in divs:
    soup = BeautifulSoup(str(div), 'html.parser')
    # Get course title from h3 tag
    h3 = soup.find('h3')
    text = h3.text.split()
    name = text[0] + " " + text[1]
    # Get credits from ng-pluralize tag
    ng_pluralize = soup.find('ng-pluralize')
    credits = re.search("[0-9]+", ng_pluralize.text)[0]
    # Create course dictionary and add to array
    course = {name: credits}
    if course not in courses:
        courses.append(course)

print(json.dumps(courses))