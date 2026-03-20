from datetime import datetime
from odfdo import Document
import subprocess
import os

def makeFolder(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

def convert_to_pdf(input_file, output_dir):
    command = [
        "soffice",
        "--headless",
        "--convert-to", "pdf",
        input_file,
        "--outdir", output_dir
    ]

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("Conversion successful!")
        print(result.stdout)
        
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        print(f"Stderr: {e.stderr}")

odt_name = "cover_letter.odt"

now = datetime.now()
date = now.strftime("%d.%m.%Y")
company = input("Company you are applying to: ").rstrip()
role = input("Role you are applying to: ").rstrip()
country = input("Country you are applying to: ").rstrip()
folder_name = company.replace(" ", "_")
makeFolder(folder_name)

doc = Document('template.odt')
body = doc.body

body.replace("{{date}}", date)
body.replace("{{role}}", role)
body.replace("{{company}}", company)
body.replace("{{country}}", country)

doc.save(f'{folder_name}/{odt_name}')
convert_to_pdf(f"{folder_name}/{odt_name}", folder_name)
