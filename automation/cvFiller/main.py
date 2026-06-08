from datetime import datetime
from pypdf import PdfReader
from odfdo import Document, Body
from odfdo.body import Text
import subprocess
import os
import re


EMAIL_ES_TEMPLATE = "email_es_template.txt"
EMAIL_EN_TEMPLATE = "email_en_template.txt"
ODT_OUTPUT_NAME = "cover_letter.odt"
ODT_TEMPLATE_DEV = "templateDEV.odt"
ODT_TEMPLATE_SYS = "templateSYS.odt"
LETTER_FIELDS = ["company", "role"]
EMAIL_FIELDS = ["company", "role"]
DEFAULT_COUNTRY = "Germany"


def are_fields_cleared(pdf_path):
    """
    Reads a PDF file and asserts that no dynamic template fields
    matching {{ word }} or {{word}} are left behind.
    """
    reader = PdfReader(pdf_path)

    full_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text

    template_pattern = r"\{\{\s*(.+?)\s*\}\}"

    found_fields = re.findall(template_pattern, full_text)

    assert not found_fields, f"Unfilled template fields found in PDF: {found_fields}"


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
    data = {val: input(f"{val}: ") for val in args}
    data["date"] = datetime.now().strftime("%d.%m.%Y")
    return data


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


def process_letter(template: str, field_data: dict[str, str]) -> None:
    folder_name = field_data["company"].replace(" ", "_")
    makeFolder(folder_name)

    doc = Document(template)
    body = doc.body

    replace_fields(body, field_data)

    pdf_folder_path = f"{folder_name}/{ODT_OUTPUT_NAME}"
    pdf_path = f"{folder_name}/cover_letter.pdf"

    doc.save(pdf_folder_path)
    convert_to_pdf(pdf_folder_path, folder_name)
    are_fields_cleared(pdf_path)


def process_email(template: str, field_data: dict[str, str]):

    with open(template) as f:
        email = f.read()
        for key, val in field_data.items():
            placeholder = "{{" + key + "}}"
            email = email.replace(placeholder, val)
        return email


if __name__ == "__main__":
    mode = input("1) Spanish Email\n2) English options")
    if mode == "1":
        print(process_email(EMAIL_ES_TEMPLATE, get_job_details(*EMAIL_FIELDS)))

    elif mode == "2":
        option = input("1) Development\n2) Systems\n")
        template = ODT_TEMPLATE_DEV if option == 1 else ODT_TEMPLATE_SYS

        option = input("1) letter and email\n2) letter\n3) email\n")
        if option == "1":  # both
            fields = set(LETTER_FIELDS + EMAIL_FIELDS)
            fields = get_job_details(*fields)
            fields["country"] = DEFAULT_COUNTRY
            process_letter(template, fields)
            email = process_email(EMAIL_EN_TEMPLATE, fields)
            print(email)
        elif option == "2":  # letter
            fields = get_job_details(*LETTER_FIELDS)
            fields["country"] = DEFAULT_COUNTRY
            process_letter(template, fields)
        elif option == "3":  # email
            fields = get_job_details(*EMAIL_FIELDS)
            fields["country"] = DEFAULT_COUNTRY
            email = process_email(EMAIL_EN_TEMPLATE, fields)
            print(email)
        else:
            print("Invalid input given")
    else:
        print("No proper option selected")
