# kinda slow


import pdfplumber
import re
from PyPDF2 import PdfReader, PdfWriter

def find_all_schedules(pdf_path):
    schedules = set()

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text:
                continue

            lines = text.split('\n')
            for line in lines:
                match = re.search(r'Schedule\s+[A-Z]', line.strip())
                if match:
                    schedules.add(match.group().strip())

    return sorted(schedules)

def extract_subheadings_with_pages(pdf_path, schedule_heading="Schedule A"):
    subheading_dict = {}
    found_schedule = False

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text:
                continue

            lines = text.split('\n')

            for line in lines:
                # Check for the Schedule Heading
                if schedule_heading.lower() in line.lower():
                    found_schedule = True
                    continue

                if found_schedule:
                    # Stop if we reach next Schedule (e.g., Schedule B)
                    if re.match(r'Schedule\s+[B-Z]', line.strip(), re.IGNORECASE):
                        return subheading_dict

                    # Extract subheading and page number (e.g., "Subheading Name ............. 12")
                    match = re.match(r'^(.*?)[\s\.]+(\d+)$', line.strip())
                    if match:
                        title, page_num = match.groups()
                        subheading_dict[title.strip()] = int(page_num)

    return subheading_dict


def extract_pdf_subset(input_pdf_path, output_pdf_path, start_page, end_page):
    """
    Extracts pages from start_page to end_page (1-indexed, inclusive).
    """
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    for i in range(start_page - 1, end_page):
        if i < len(reader.pages):
            writer.add_page(reader.pages[i])

    with open(output_pdf_path, 'wb') as f_out:
        writer.write(f_out)

    print(f"Extracted PDF saved to: {output_pdf_path}")


# === Example usage ===
if __name__ == "__main__":
    pdf_path = "/Users/parthshukla/Documents/_working_space/gaidp-l-la-ma-mia/code/src/backend/data/FR_Y-14Q20240331_i.pdf"
    schedules = find_all_schedules(pdf_path=pdf_path)
    print(schedules)
    schedule = "Schedule B"

    # 1. Extract subheadings under Schedule A
    headings = extract_subheadings_with_pages(pdf_path, schedule_heading=schedule)
    print("Extracted Subheadings and Pages:", headings)

    # extract_pdf_subset(pdf_path, "extracted_part.pdf", start_page=12, end_page=16)
