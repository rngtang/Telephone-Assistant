# This program updates the PDF file that we use as our knowledge base.
# We implemented a cron job to run this program in the background and it starts automatically every time we turn on the Raspberry Pi

import requests
import pathlib
from fpdf import FPDF
from PyPDF2 import PdfReader, PdfMerger

# URLs being used for current information
StudioUrl = 'https://shiftr-api.colab.duke.edu/publicCalendars/digitalSign/current/CoLab%20Studios/TEC'
StudentDevsUrl = 'https://shiftr-api.colab.duke.edu/publicCalendars/digitalSign/current/Colab%20Student%20Developer/TEC%20Office%20Hours'
rootClasses = 'https://api.pathways.duke.edu/api/v1/signage_sync?location=1'

# Running with Chron needs absolute directory -> build absolute directory based on context
script_directory = pathlib.Path(__file__).parent.resolve()
base_dir = str(script_directory) + "/../files/"

# Gets the next 5 Roots Classes
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

# Builds the PDF for each URL 
def get(heading, info, title):
    print(info)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=12)
    pdf.write(5, heading)
    pdf.write(5, info)
    pdf.output(base_dir + title)

# Builds a PDF for each URL. Then combines these URLs with main (static) information doc.
def main(): 
    print("Checking APIs")

    # Roots Classes
    roots = getRoots(rootClasses)
    get("These are the Upcoming Roots Classes: \n", roots, "Upcoming_Roots.pdf")

    # Student Developers
    dev = getInfo(StudentDevsUrl)
    get("Student developers can help anyone with software issues. \n These are the Current Student Developers (part-time help with software): \n", dev, "Current_Student_Devs.pdf")

    # Studio Workers
    studio = getInfo(StudioUrl)
    get("The studio workers can help anyone use the 3d printer, laser cutter, and other physical tools. \n These are the Current Studio Workers (part-time help with the studio and garage): \n", studio, "Current_Studio_Workers.pdf")

    # Merge all documents
    try: 
        print("Collecting documents...")
        filenames = [base_dir + "No_Questions.pdf", base_dir + "Upcoming_Roots.pdf", base_dir + "Current_Studio_Workers.pdf", base_dir + "Current_Student_Devs.pdf"]
        
        merger = PdfMerger()
        for filename in filenames:
            read = PdfReader(filename)
            merger.append(read)
        
        merger.write(base_dir + "All_Info.pdf")
        merger.close()

        print("Finished!")

    except Exception as error:
        print("All_Info.pdf not updated: ", error)

if __name__ == "__main__":
    main()


