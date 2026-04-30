from datetime import datetime
from typing import Sequence
from odfdo import Document, Body
from odfdo.body import Text
import subprocess
import os


def makeFolder(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


def convert_to_pdf(input_file, output_dir):
    command = [
        "soffice",
        "--headless",
        "--convert-to",
        "pdf",
        input_file,
        "--outdir",
        output_dir,
    ]

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("Conversion successful!")
        print(result.stdout)

    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        print(f"Stderr: {e.stderr}")


def get_job_details(*args: str) -> dict[str, str]:
    """Given a sequence of fields, asks the user for the information and
    returns a dictionary with the answers"""
    return {val: input(f"{val}: ") for val in args}


def replace_fields(template: Text | Body | str, data: dict[str, str]):
    """Placeholders inside of the template are replaced in-place with
    information contained in data"""
    if isinstance(template, (Text, Body)):
        for key, val in data.items():
            placeholder = "{{" + key + "}}"
            template.replace(placeholder, val)
    else:
        processed_template = template
        for key, val in data.items():
            placeholder = "{{" + key + "}}"
            processed_template = processed_template.replace(placeholder, val)


def process_letter(template: str, fields: Sequence[str]) -> None:
    data = get_job_details(*fields)
    data["date"] = datetime.now().strftime("%d.%m.%Y")

    folder_name = data["company"].replace(" ", "_")
    makeFolder(folder_name)

    doc = Document(template)
    body = doc.body

    replace_fields(body, data)

    doc.save(f"{folder_name}/{ODT_OUTPUT_NAME}")
    convert_to_pdf(f"{folder_name}/{ODT_OUTPUT_NAME}", folder_name)


def process_email(template: str, fields: Sequence[str]):
    data = get_job_details(*fields)
    data["date"] = datetime.now().strftime("%d.%m.%Y")

    with open(template) as f:
        email = f.read()
        for key, val in data.items():
            placeholder = "{{" + key + "}}"
            email = email.replace(placeholder, val)
        return email


EMAIL_ES_TEMPLATE = "email_es_template.txt"
EMAIL_EN_TEMPLATE = "email_en_template.txt"
ODT_OUTPUT_NAME = "cover_letter.odt"
ODT_TEMPLATE_DEV = "templateDEV.odt"
ODT_TEMPLATE_SYS = "templateSYS.odt"
LETTER_FIELDS = ("company", "role", "country")
EMAIL_FIELDS = ("company", "role")

if __name__ == "__main__":
    option = input("1) Development\n2) Systems\n")
    template = ODT_TEMPLATE_DEV if option == 1 else ODT_TEMPLATE_SYS

    option = input("1) letter and email\n2) letter\n3) email\n")
    if option == "1":  # both
        process_letter(template, LETTER_FIELDS)
        email = process_email(EMAIL_EN_TEMPLATE, EMAIL_FIELDS)
        print(email)
    elif option == "2":  # letter
        process_letter(template, LETTER_FIELDS)
    elif option == "3":  # email
        email = process_email(EMAIL_ES_TEMPLATE, EMAIL_FIELDS)
        print(email)
    else:
        print("Invalid input given")
