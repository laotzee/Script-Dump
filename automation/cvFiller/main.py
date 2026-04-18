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


def process_letter() -> None:
    fields = ("company", "role", "country")
    data = get_job_details(*fields)
    data["date"] = datetime.now().strftime("%d.%m.%Y")

    folder_name = data["company"].replace(" ", "_")
    makeFolder(folder_name)

    doc = Document("template.odt")
    body = doc.body

    for key, val in data.items():
        placeholder = "{{" + key + "}}"
        body.replace(placeholder, val)

    doc.save(f"{folder_name}/{odt_name}")
    convert_to_pdf(f"{folder_name}/{odt_name}", folder_name)


odt_name = "cover_letter.odt"

if __name__ == "__main__":
    process_letter()
