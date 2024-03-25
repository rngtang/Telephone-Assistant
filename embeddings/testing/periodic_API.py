import requests
import schedule
import time
from fpdf import FPDF
from PyPDF2 import PdfFileMerger

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

def create_pdf(text, name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=12)
    pdf.write(5, text)
    pdf.output(f'{name}.pdf')

def roots_job():
    info = getRoots(rootClasses)
    create_pdf(info, "Upcoming_Roots_Classes")

def studev_job():
    info = getInfo(StudentDevsUrl)
    create_pdf(info, "Current_Student_Devs")

def studio_job():
    info = getInfo(StudioUrl)
    create_pdf(info, "Current_Studio_Workers")

# schedule.every().day.at("08:00").do(roots_job)
schedule.every(1).minutes.do(roots_job)
schedule.every(1).minutes.do(studev_job)
schedule.every(1).minutes.do(studio_job)

while True:
    schedule.run_pending()
    time.sleep(30)  # Check every minute
