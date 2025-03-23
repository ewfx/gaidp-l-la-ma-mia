"""
Rule based Index Extractor for PDF Documents.
Expects Schedules to be listed under which specific categories may be mentioned
"""

import os
import pdfplumber
import csv
import requests

# kinda slow

import pdfplumber
import re
from PyPDF2 import PdfReader, PdfWriter

def find_all_schedules(pdf_path, pageToSearchTill):
    schedules = set()

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            if i >= pageToSearchTill:
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

def extract_subheadings_with_pages(pdf_path, pageToSearchTill, schedule_heading="Schedule A"):
    subheading_dict = {}
    found_schedule = False
    found_next_schedule = False

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            if i >= pageToSearchTill:
                break
            text = page.extract_text()
            if not text:
                continue

            lines = text.split('\n')

            for line in lines:
                # Check for the Schedule Heading
                if not found_schedule and schedule_heading.lower() in line.lower():
                    match = re.match(r'^(.*?)[\s\.]+(\d+)$', line.strip())
                    if match:
                        title, page_num = match.groups()
                        subheading_dict[title.strip()] = int(page_num)
                    found_schedule = True
                    continue

                if found_schedule:
                        # Stop if we reach next Schedule (e.g., Schedule B)
                    if not found_next_schedule and re.match(r'Schedule\s+[B-Z]', line.strip(), re.IGNORECASE):
                        found_next_schedule = True
                        match = re.match(r'^(.*?)[\s\.]+(\d+)$', line.strip())
                        if match:
                            _, page_num = match.groups()
                            subheading_dict["END"] = int(page_num)
                    if not found_next_schedule or re.search(fr'SUPPORTING DOCUMENTATION FOR {re.escape(schedule_heading)}', line.strip(), re.IGNORECASE):
                        # Extract subheading and page number (e.g., "Subheading Name ............. 12")
                        match = re.match(r'^(.*?)[\s\.]+(\d+)$', line.strip())
                        if match:
                            title, page_num = match.groups()
                            subheading_dict[title.strip()] = int(page_num)

    return subheading_dict

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
                        return heading.strip(), int(page_num)-1

    return None, None

def get_page_range(contents_dict, schedule, subheading):
    """
    Retrieves the start and end page range for a given schedule and subheading.
    """
    if schedule in contents_dict and subheading in contents_dict[schedule]:
        start_page = contents_dict[schedule][subheading]
        
        # Find the next key in order that is not "Supporting documentation"
        keys = list(contents_dict[schedule].keys())
        current_index = keys.index(subheading)
        end_page = None
        
        for next_key in keys[current_index + 1:]:
            if "supporting documentation" not in next_key.lower():
                end_page = contents_dict[schedule][next_key]
                break
        
        # If no valid next key is found, default to the same as start_page
        if end_page is None:
            end_page = start_page
        
        return start_page, end_page
    else:
        raise ValueError(f"Subheading '{subheading}' not found in schedule '{schedule}'.")

def extract_index(pdf_path):
    _, pageToSearchTill = find_contents_and_first_heading(pdf_path)
    schedules = find_all_schedules(pdf_path, pageToSearchTill)
    contents_dict = {}
    contents_dict["Name"] = pdf_path.split("/")[-1]
    contents_dict["Schedules"] = []
    for schedule in schedules:
        contents_dict["Schedules"].append({"Name": schedule, "Categories": []})
        # 1. Extract subheadings under Schedule A
        headings = extract_subheadings_with_pages(pdf_path, pageToSearchTill, schedule_heading=schedule)
        for heading, page in headings.items():
            contents_dict["Schedules"][-1]["Categories"].append({"Name": heading, "Page": page})
        # print(f"Extracted Subheadings and Pages for {schedule}:", headings)

    print(contents_dict)

extract_index("/Users/agastya/Documents/Projects/gaidp-l-la-ma-mia/code/src/backend/data/FR_Y-14Q20240331_i.pdf")