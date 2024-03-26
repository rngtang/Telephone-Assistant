import requests
import schedule
import time
from fpdf import FPDF
from PyPDF2 import PdfReader, PdfMerger


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
    info = getRoots(rootClasses)
    print(info)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=12)
    pdf.write(5, "These are the Upcoming Roots Classes: \n")
    pdf.write(5, info)
    pdf.output(f'../files/Upcoming_Roots_Classes.pdf')

def studev_job():
    info = getInfo(StudentDevsUrl)
    print(info)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=12)
    pdf.write(5, "These are the Current Student Developers (part-time help with software): \n")
    pdf.write(5, info)
    pdf.output(f'../files/Current_Student_Devs.pdf')

def studio_job():
    info = getInfo(StudioUrl)
    print(info)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=12)
    pdf.write(5, "These are the Current Studio Workers (part-time help with the studio and garage): \n")
    pdf.write(5, info)
    pdf.output(f'../files/Current_Studio_Workers.pdf')

schedule.every().day.at("08:00").do(roots_job)
# schedule.every(1).minutes.do(roots_job)
schedule.every(20).minutes.do(studev_job)
schedule.every(20).minutes.do(studio_job)

while True:
    schedule.run_pending()
    time.sleep(1200)  # Check every 20 minutes

    print("Collecting documents...")
    # Merges all documents together
    filenames = ["../files/FormattedK.pdf", "../files/Upcoming_Roots_Classes.pdf", "../files/Current_Studio_Workers.pdf", "../files/Current_Student_Devs.pdf"]
    merger = PdfMerger()
    for filename in filenames:
        merger.append(PdfReader(open(filename, 'rb')))
    merger.write("../files/All_Info.pdf")
