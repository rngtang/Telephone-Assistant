import requests
import schedule
import time

StudioUrl = 'https://shiftr-api.colab.duke.edu/publicCalendars/digitalSign/current/CoLab%20Studios/TEC'
StudentDevsUrl = 'https://shiftr-api.colab.duke.edu/publicCalendars/digitalSign/current/Colab%20Student%20Developer/TEC%20Office%20Hours'
rootClasses = 'https://api.pathways.duke.edu/api/v1/signage_sync?location=1'

def getRoots():
    response = requests.get(rootClasses)
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
    print("Upcoming Roots Classes:", classes)

def studio_job():
    StudioInfo = getInfo(StudioUrl)
    print("Current Student Studio Workers:", StudioInfo)

def studev_job():
    StuDevInfo = getInfo(StudentDevsUrl)
    print("Current Student Developers:", StuDevInfo)

schedule.every().day.at("08:00").do(roots_job)
schedule.every(1).minutes.do(studio_job)
schedule.every(1).minutes.do(studev_job)

while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
