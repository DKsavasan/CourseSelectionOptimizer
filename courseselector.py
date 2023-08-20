import requests
from bs4 import BeautifulSoup
from googlesearch import search
import itertools
from pprint import pprint

#User Inputs
hub_code = {"Philosophical Inquiry and Life's Meaning":'A',
            "Aesthetic Exploration":"B",
            "Historical Consciousness":"C",
            "Quantitative Reasoning I": "G",
            "Q2": "H",
            "S1": "D",
            "Scientific Inquiry II":"F",
            "Social Inquiry I": "E",
            "Social Inquiry II":"P",
            "The Individual in Community": "I",
            "G": "J",
            "E": "K",
            "C": "1",
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
            print(course_search_query)
            break

    else:
        print('How many do you want??')

#Access the course search website
course_search_website = requests.get(str(course_search_query))
course_search_html = course_search_website.content
course_search_content = BeautifulSoup(course_search_html, 'html.parser')

#Create the course dictionary
class_details = {}


#Get class name and sections link
class_code = course_search_content.find_all('h6')
class_name = course_search_content.find_all('h2')
class_link = course_search_content.find_all('a', class_="coursearch-result-sections-link", href=True )

for a,b,c in zip(class_code,class_name,class_link):
    class_details[a.text] = [b.text, "https://www.bu.edu" + c['href']]


#Get proffesor names
for key, vals in zip(class_details.keys(), class_details.values()):
    w = requests.get(vals[1])
    h = w.content
    c = BeautifulSoup(h, 'html.parser')

    for line in c.find_all('tr', class_='first-row'):
        if 'LEC' in line.text or 'IND' in line.text:
            try:
                prof = (line.find_all(rowspan='1')[2]).text
            except IndexError:
                prof = (line.find_all(rowspan='2')[2]).text
            if [prof] not in class_details[key] and prof != 'Staff' and prof != 'TBA' and prof != '':
                class_details[key] += [[prof]]

#-----------------------------------------------------------------------------------------------------------------------------------------------
#Getting rate my proffesors link

for i in class_details:
    if len(class_details[i]) < 3:
        del class_details[i]
    
    elif len(class_details[i]) > 3:
        for k in range(1, len(class_details[i]) - 1):
            pass
    
    elif len(class_details[i]) == 3:
        emptystr = ''
        query = 'ratemyprofessors ' + emptystr.join(class_details[i][-1]) + ' ' + i[-3:] + ' Boston University'
  

        for link in search(query, lang='en', num=10, stop=10, pause=2):
            if 'ShowRatings' in link and 'ratemyprofessors' in link:
                rating_website = link
                break
        
        ratemyprof_website = requests.get(str(rating_website))
        html_ratemyprof = ratemyprof_website.content
        content_ratemyprof = BeautifulSoup(html_ratemyprof, 'html.parser')

        quality = content_ratemyprof.find('div', class_= 'RatingValue__Numerator-qw8sqy-2 liyUjw').get_text()
        num_ratings = content_ratemyprof.find('a', href='#ratingsList').get_text()


        dif_level = content_ratemyprof.find_all('div', class_= 'FeedbackItem__FeedbackNumber-uof32n-1 kkESWs')
        vals = []
        for num in dif_level:
            vals.append(num.get_text())
        
        rating = (quality, num_ratings[:-8], vals[0], vals[1])
        score = (float(quality) * 20) + int(vals[0][:-1]) - (float(vals[1]) * 20)

        class_details[i][2] += [float(score)]
        class_details[i][2] += [rating]

pprint(class_details)







'''
for link in search(query, lang='en', num=10, stop=10, pause=2):
    if 'ShowRatings' in link and 'ratemyprofessors' in link:
        rating_website = link
        break

#Accesing the website
ratemyprof_website = requests.get(str(rating_website))
html_ratemyprof = ratemyprof_website.content
content_ratemyprof = BeautifulSoup(html_ratemyprof, 'html.parser')

#Getting Overall Quality and amount of ratings
quality = content_ratemyprof.find('div', class_= 'RatingValue__Numerator-qw8sqy-2 liyUjw').get_text()
num_ratings = content_ratemyprof.find('a', href='#ratingsList').get_text()
 
#Getting  take again rate and level of diffuculity
dif_level = content_ratemyprof.find_all('div', class_= 'FeedbackItem__FeedbackNumber-uof32n-1 kkESWs')
vals = []
for num in dif_level:
    vals.append(num.get_text())

'''

