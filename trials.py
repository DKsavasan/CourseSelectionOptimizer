import requests
from bs4 import BeautifulSoup
import itertools


#If you know the class code
""" course = {}

#Asking the course code to the user
while True:
    course_code = str(input('Enter the class code (cas-xx-123):'))
    if len(course_code) !=10 or course_code[3] != '-' or course_code[6] != '-':
        print('Please enter a valid class code!')
    else:
        course['Code'] = course_code
        break

#Accesing the Website
website_link = 'https://www.bu.edu/academics/cas/courses/' + course_code
website = requests.get(str(website_link))
html_website = website.content
html_content = BeautifulSoup(html_website, 'html.parser')

#Getting the course name
title = html_content.find_all('h1')
for elem in title:
    if 'http' not in elem:
        course['Title'] = elem.text

#Getting the Instructer name
lecturers = html_content.find_all('td')
course['Lecturers'] = []

for lec in lecturers:
    lec = lec.text
    if lec.isalpha() and (len(lec) > 1):
        if lec not in course['Lecturers']:
            course['Lecturers'].append(lec)

#Getting hub units
hubs = html_content.find("ul", class_="cf-hub-offerings")
course['Hub_units'] = []
for hub in hubs.children:
    if len(hub.text) != 1:
        course['Hub_units'].append(hub.text)"""

'----------------------------------------------------------------'



hub_code = {"Philosophical Inquiry and Life's Meaning":'A',
            "Aesthetic Exploration":"B",
            "Historical Consciousness":"C",
            "Quantitative Reasoning I": "G",
            "Quantitative Reasoning II": "H",
            "Scientific Inquiry I": "D",
            "Scientific Inquiry II":"F",
            "Social Inquiry I": "E",
            "Social Inquiry II":"P",
            "The Individual in Community": "I",
            "Global Citizenship and Intercultural Literacy": "J",
            "Ethical Reasoning": "K",
            "Critical Thinking": "1",
            "Research and Information Literacy": "2",
            "Teamwork/Collaboration": "3",
            "Creativity?Innovation": "4",
            "First-year writing Seminar": "L",
            "Writing, Research, and Inquiry": "M",
            "Writing-Intensive": "6",
            "Oral and Signed Communications": "N",
            "Digital/Multimedia Expression": "O"}

while True:
    hub_number = str(input("Enter the number of hubs you want the class to have (1-3):"))
    if hub_number == '1':
        hub1 = str(input("Enter which hub you want:"))
        if hub1 not in hub_code:
            print('There is already enough hubs dont make a new one...')
        else:
            course_search_query = "https://www.bu.edu/phpbin/course-search/search.php?page=w0&pagesize=-1&adv=1&nolog=&search_adv_all=&yearsem_adv=2022-FALL&credits=*&pathway=&hub_match=all&hub%5B%5D="\
                + str(hub_code[hub1]) + "&pagesize=-1"
            print(course_search_query)
            break
    elif hub_number == '2':
        hub1 = str(input("Enter the first hub you want:"))
        hub2 = str(input("Enter the second hub you want:"))
        if hub1 not in hub_code or hub2 not in hub_code:
            print('Enter a correct hub!')
        else:
            course_search_query = "https://www.bu.edu/phpbin/course-search/search.php?page=w0&pagesize=-1&adv=1&nolog=&search_adv_all=&yearsem_adv=2022-FALL&credits=*&pathway=&hub_match=all&hub%5B%5D="\
                + str(hub_code[hub1]) + "&hub%5B%5D=" + str(hub_code[hub2]) + "&pagesize=-1"
            print(course_search_query)
            break
    elif hub_number == '3':
        hub1 = str(input("Enter the first hub you want:"))
        hub2 = str(input("Enter the second hub you want:"))
        hub3 = str(input("Enter the third hub you want:"))
        if hub1 not in hub_code or hub2 not in hub_code or hub3 not in hub_code:
            print('Enter correctly!')
        else:
            course_search_query = "https://www.bu.edu/phpbin/course-search/search.php?page=w0&pagesize=-1&adv=1&nolog=&search_adv_all=&yearsem_adv=2022-FALL&credits=*&pathway=&hub_match=all&hub%5B%5D="\
                + str(hub_code[hub1]) + "&hub%5B%5D=" + str(hub_code[hub2]) + "&hub%5B%5D=" + str(hub_code[hub3]) + "&pagesize=-1"
      
            break
    else:
        print('How many do you want??')

course_search_website = requests.get(str(course_search_query))
course_search_html = course_search_website.content
course_search_content = BeautifulSoup(course_search_html, 'html.parser')




class_details = {}
class_code = course_search_content.find_all('h6')
class_name = course_search_content.find_all('h2')
class_link = course_search_content.find_all('a', class_="coursearch-result-sections-link", href=True )

for a,b,c in zip(class_code,class_name,class_link):
    class_details[a.text] = [b.text, "https://www.bu.edu" + c['href']]


for key, vals in zip(class_details.keys(), class_details.values()):
    w = requests.get(vals[1])
    h = w.content
    c = BeautifulSoup(h, 'html.parser')

    for line in c.find_all('tr', class_='first-row'):
        if 'LEC' in line.text or 'IND' in line.text:
            try:
                prof = (line.find_all(rowspan='1')[2]).text
                print(prof)
            except IndexError:
                prof = (line.find_all(rowspan='2')[2]).text
            if prof not in class_details[key] and prof != 'Staff':
                class_details[key] += [prof]

print(class_details)






            
            

    













