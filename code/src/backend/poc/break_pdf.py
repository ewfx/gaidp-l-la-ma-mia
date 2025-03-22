# kinda slow


import pdfplumber
import re
from PyPDF2 import PdfReader, PdfWriter

def find_all_schedules(pdf_path, pageToSearchTill):
    schedules = set()

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            if i > pageToSearchTill:
                break
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


def find_contents_and_first_heading(pdf_path):
    """
    Finds the first occurrence of 'Contents' or similar headings in the PDF, extracts the first heading under it,
    and determines its page number.
    """
    index_keywords = [r'\bContents\b', r'\bIndex\b', r'\bTable of Contents\b', r'\bTOC\b']
    with pdfplumber.open(pdf_path) as pdf:
        found_contents = False

        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text:
                continue

            lines = text.split('\n')
            for line in lines:
                # Check for the first occurrence of any index-related keyword
                if not found_contents and any(re.search(keyword, line, re.IGNORECASE) for keyword in index_keywords):
                    found_contents = True
                    continue

                # If an index-related keyword was found, look for the first heading under it
                if found_contents:
                    # Assume headings are lines with larger font sizes or specific patterns
                    match = re.match(r'^(.*?)[\s\.]+(\d+)$', line.strip())
                    if match:
                        heading, page_num = match.groups()
                        return heading.strip(), int(page_num)

    return None, None


# === Example usage ===
if __name__ == "__main__":
    pdf_path = "/Users/parthshukla/Documents/_working_space/gaidp-l-la-ma-mia/code/src/backend/data/FR_Y-14Q20240331_i.pdf"
    # _, pageToSearchTill = find_contents_and_first_heading(pdf_path)
    # print("Page to search till:", pageToSearchTill)
    # schedules = find_all_schedules(pdf_path, pageToSearchTill)
    # print(schedules)
    # schedule = "Schedule B"

    # for schedule in schedules:
    #     # 1. Extract subheadings under Schedule A
    #     headings = extract_subheadings_with_pages(pdf_path, schedule_heading=schedule)
    #     print(f"Extracted Subheadings and Pages for {schedule}:", headings)

    extract_pdf_subset(pdf_path, "extracted_part.pdf", start_page=17, end_page=22)
