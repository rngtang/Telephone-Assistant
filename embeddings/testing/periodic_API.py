import requests
# import schedule
import time
from fpdf import FPDF
from PyPDF2 import PdfReader, PdfMerger


StudioUrl = 'https://shiftr-api.colab.duke.edu/publicCalendars/digitalSign/current/CoLab%20Studios/TEC'
StudentDevsUrl = 'https://shiftr-api.colab.duke.edu/publicCalendars/digitalSign/current/Colab%20Student%20Developer/TEC%20Office%20Hours'
rootClasses = 'https://api.pathways.duke.edu/api/v1/signage_sync?location=1'

base_dir = "/home/colabdev/Desktop/telephone-assistant/embeddings/files/"

# Gets the next 5 root classes
def getRoots(url):
    response = requests.get(url)
    classes = ""

    if(response.status_code == 200):
        data = response.json()
        for c in data:
            classes = classes + ", " + c["course_name"] + ": " + c["start"] 
    return classes

# Gets the current workers
def getInfo(url):
    response = requests.get(url)
    workers = ""

    if response.status_code == 200:
        data = response.json()
        for worker in data:
            workers = workers + ", " + worker["user_name"]
    return workers[2:]

def get(heading, info, title):
    print(info)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=12)
    pdf.write(5, heading)
    pdf.write(5, info)
    pdf.output(base_dir + title)

def main(): 
    print("Checking APIs")
    roots = getRoots(rootClasses)
    get("These are the Upcoming Roots Classes: \n", roots, "Upcoming_Roots.pdf")

    dev = getInfo(StudentDevsUrl)
    get("Student developers can help anyone with software issues. These are the Current Student Developers (part-time help with software): \n", dev, "Current_Student_Devs.pdf")

    studio = getInfo(StudioUrl)
    get("The studio workers can help anyone use the 3d printer, laser cutter, and other physical tools. These are the Current Studio Workers (part-time help with the studio and garage): \n", studio, "Current_Studio_Workers.pdf")


    print("Collecting documents...")
    filenames = [base_dir + "No_Questions.pdf", base_dir + "Upcoming_Roots.pdf", base_dir + "Current_Studio_Workers.pdf", base_dir + "Current_Student_Devs.pdf"]
    
    merger = PdfMerger()
    for filename in filenames:
        read = PdfReader(filename)
        merger.append(read)
    
    merger.write(base_dir + "All_Info.pdf")
    merger.close()


    print("Finished!")

if __name__ == "__main__":
    main()


