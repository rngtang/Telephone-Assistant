import requests
import schedule
import time
import pdfkit

StudioUrl = 'https://shiftr-api.colab.duke.edu/publicCalendars/digitalSign/current/CoLab%20Studios/TEC'
StudentDevsUrl = 'https://shiftr-api.colab.duke.edu/publicCalendars/digitalSign/current/Colab%20Student%20Developer/TEC%20Office%20Hours'
rootClasses = 'https://api.pathways.duke.edu/api/v1/signage_sync?location=1'

def getRoots(url):
    response = requests.get(url)
    classes = ""

    if(response.status_code == 200):
        data = response.json()
        for c in data:
            classes = classes + ", " + c["course_name"] + ": " + c["start"] 
    return classes

def getInfo(url):
    response = requests.get(url)
    workers = ""

    if response.status_code == 200:
        data = response.json()
        for worker in data:
            workers = workers + ", " + worker["user_name"]
    return workers[2:]

def roots_job():
    classes = getRoots(rootClasses)
    pdfkit.from_string(str(classes), "Upcoming_Roots_Classes.pdf")
    # try out pdfkit.from_url('http://google.com', 'out.pdf')
    print("Upcoming Roots Classes:", classes)

def studev_job():
    info = getInfo(StudentDevsUrl)
    pdfkit.from_string(str(info), "Current_Studio_Workers.pdf")
    print("Upcoming Roots Classes:", info)

def studio_job():
    info = getRoots(rootClasses)
    pdfkit.from_string(str(info), "Current_Studio_Workers.pdf")
    print("Curren Studio Workers:", info)

# schedule.every().day.at("08:00").do(roots_job)
schedule.every(1).minutes.do(roots_job)
schedule.every(1).minutes.do(studev_job)
schedule.every(1).minutes.do(studio_job)

while True:
    schedule.run_pending()
    time.sleep(30)  # Check every minute
