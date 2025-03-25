import os
import re
from fastapi import APIRouter, UploadFile, File, HTTPException
from services.RuleGen.extract_db_queries import process_rules_and_generate_queries
from services.RuleGen.extract_index import extract_index
from services.anomaly_detection import detect_anomalies
from services.base_mongo_service import BaseMongoService  # Import BaseMongoService
import shutil
from dto.response_dto import ResponseDTO as dto
from datetime import datetime
import pandas as pd
import uuid
from pymongo import MongoClient
from services.RuleGen.extract_profiling_rules import extract_profiling_rules  # Import the function

router = APIRouter(prefix="/data", tags=["Anomaly Detection"])

@router.post("/uploadcsv")
async def upload_csv(file: UploadFile = File(...), pdfName: str = None, schedule: str = None, category: str = None):
    """
    Endpoint to upload a CSV file and store it in a writable directory with a timestamped filename.

    Args:
        file (UploadFile): The uploaded CSV file.

    Returns:
        dict: A dictionary containing the stored filename.
    """
    # Use a writable directory (e.g., /tmp or a directory within the project)
    upload_dir = "./.tmp"  # Change this to a writable directory
    os.makedirs(upload_dir, exist_ok=True)

    # Generate a timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{os.path.splitext(file.filename)[0]}_{timestamp}{os.path.splitext(file.filename)[1]}"
    file_path = os.path.join(upload_dir, filename)

    # Save the uploaded file
    try:
        with open(file_path, "wb") as temp_file:
            shutil.copyfileobj(file.file, temp_file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save the uploaded file: {str(e)}")

    # Store the CSV records into MongoDB
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Add a row_number column to the DataFrame
        df["row_number"] = range(1, len(df) + 1)

        # Remove the .pdf extension from pdfName
        sanitized_pdf_name = re.sub(r'\.pdf$', '', pdfName, flags=re.IGNORECASE)

        # Generate the sanitized collection name
        collection_name = f"{sanitized_pdf_name}_{schedule}_{category}"
        collection_name = re.sub(r'[^a-zA-Z0-9_]', '', collection_name)  # Keep only alphanumeric characters and underscores

        # Generate a unique collection name
        collection_name = f"{collection_name}_{uuid.uuid4().hex}"

        # Initialize MongoDB client and service
        mongo_client = MongoClient(os.environ.get("MONGO_URI"))  # Replace with your MongoDB connection string
        mongo_service = BaseMongoService(mongo_client, collection_name)

        # Convert DataFrame to a list of dictionaries and insert into MongoDB
        records = df.to_dict(orient="records")
        mongo_service.create_many(records)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store CSV records in MongoDB: {str(e)}")

    return dto(isSuccess=True, data={"filename": filename, "collection_name": collection_name})

@router.post("/anomaly")
async def detect_anomalies_endpoint(file: UploadFile = File(...), contamination: float = 0.01):
    """
    Endpoint to detect anomalies in an uploaded CSV file.

    Args:
        file (UploadFile): The uploaded CSV file.
        contamination (float): The proportion of anomalies in the data (default is 0.05).

    Returns:
        dict: A dictionary containing the row numbers of detected anomalies.
    """
    # Save the uploaded file to a temporary location
    temp_file_path = f"./.tmp/{file.filename}"  # Use a writable directory
    os.makedirs("./.tmp", exist_ok=True)  # Ensure the directory exists
    try:
        with open(temp_file_path, "wb") as temp_file:
            shutil.copyfileobj(file.file, temp_file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save the uploaded file: {str(e)}")

    # Call the detect_anomalies function
    try:
        anomalies = detect_anomalies(temp_file_path, contamination=contamination)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while detecting anomalies: {str(e)}")
    finally:
        # Clean up the temporary file
        os.remove(temp_file_path)

    return dto(isSuccess=True, data={"anomalies": anomalies})

@router.post("/uploadpdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Endpoint to upload a PDF file and store it as a blob in the database along with the name of the PDF.

    Args:
        file (UploadFile): The uploaded PDF file.

    Returns:
        dict: A dictionary containing the stored filename and collection name.
    """
    try:
        # Read the PDF file content
        pdf_content = await file.read()

        # Extract the PDF name from the metadata
        pdf_name = file.filename

        # Initialize MongoDB client and service
        mongo_client = MongoClient(os.environ.get("MONGO_URI"))  # Replace with your MongoDB connection string
        mongo_service = BaseMongoService(mongo_client, "Raw_PDFs")

        # Store the PDF as a blob in the database
        record = {
            "name": pdf_name,
            "pdf_blob": pdf_content,
            "uploaded_at": datetime.now()
        }
        mongo_service.create(record)

        # Extract the index and store it in the PDF_Index collection
        mongo_service = BaseMongoService(mongo_client, "PDF_Index")
        contents_dict = extract_index(pdf_name)
        mongo_service.create(contents_dict)

        # Extract the profiling rules and store them in the PDFName_Schedule_Category collection

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store PDF in MongoDB: {str(e)}")

    return dto(isSuccess=True, data={"filename": pdf_name, "collection_name": "PDF_Index"})

@router.post("/extractprofilingrules")
async def extract_profiling_rules_and_db_queries(pdfName: str = None, schedule: str = None, category: str = None):
    """
    Endpoint to extract profiling rules and db queries for a particular category.

    Args:
        pdfName (str): The name of the PDF.
        schedule (str): The schedule name.
        category (str): The category name.

    Returns:
        dict: A dictionary containing the extracted profiling rules.
    """
    try:
        if not pdfName or not schedule or not category:
            raise HTTPException(status_code=400, detail="Missing required parameters: pdfName, schedule, or category")

        # Call the extract_profiling_rules function only if rules not generated
        if not await is_rules_available(pdfName, schedule, category):
            collection_name = extract_profiling_rules(pdfName, schedule, category)
        # Remove the .pdf extension from pdfName
        sanitized_pdf_name = re.sub(r'\.pdf$', '', pdfName, flags=re.IGNORECASE)

        # Generate the sanitized collection name
        collection_name = f"{sanitized_pdf_name}_{schedule}_{category}"
        collection_name = re.sub(r'[^a-zA-Z0-9_]', '', collection_name)  # Keep only alphanumeric characters and underscores
        process_rules_and_generate_queries(collection_name)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate profiling rules: {str(e)}")

    return dto(isSuccess=True, data={"collectionName": collection_name})

@router.post("/isrulesavailbale")
async def is_rules_available(pdfName: str = None, schedule: str = None, category: str = None):
    """
    Endpoint to check if profiling rules are available.

    Args:
        pdfName (str): The name of the PDF.
        schedule (str): The schedule name.
        category (str): The category name.

    Returns:
        isSuccess: True if rules are available, False otherwise.
    """
    try:
        if not pdfName or not schedule or not category:
            raise HTTPException(status_code=400, detail="Missing required parameters: pdfName, schedule, or category")
        
        # Remove the .pdf extension from pdfName
        sanitized_pdf_name = re.sub(r'\.pdf$', '', pdfName, flags=re.IGNORECASE)

        # Generate the sanitized collection name
        collection_name = f"{sanitized_pdf_name}_{schedule}_{category}"
        collection_name = re.sub(r'[^a-zA-Z0-9_]', '', collection_name)  # Keep only alphanumeric characters and underscores

        # Check if the collection exists
        mongo_client = MongoClient(os.environ.get("MONGO_URI"))  # Replace with your MongoDB connection string
        mongo_service = BaseMongoService(mongo_client, collection_name)
        exists = mongo_service.collection_exists()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to check if rules are available: {str(e)}")

    return dto(isSuccess=True, data={"collectionName": collection_name, "exists": exists})

@router.get("/violations")
async def get_violations(pdfName: str = None, schedule: str = None, category: str = None, dataCollectionName: str = None):
    """
    Endpoint to fetch DB queries associated with profiling rules and run them against data uploaded by the user.

    Args:
        pdfName (str): The name of the PDF.
        schedule (str): The schedule name.
        category (str): The category name.
        dataCollectionName (str): The name of the collection where the data is stored.

    Returns:
        dict: A dictionary containing rows with violations, grouped by rule and column.
    """
    try:
        if not pdfName or not schedule or not category or not dataCollectionName:
            raise HTTPException(status_code=400, detail="Missing required parameters: pdfName, schedule, category, or dataCollectionName")

        # Remove the .pdf extension from pdfName
        sanitized_pdf_name = re.sub(r'\.pdf$', '', pdfName, flags=re.IGNORECASE)

        # Generate the sanitized collection name for rules
        rules_collection_name = f"{sanitized_pdf_name}_{schedule}_{category}"
        rules_collection_name = re.sub(r'[^a-zA-Z0-9_]', '', rules_collection_name)  # Keep only alphanumeric characters and underscores

        # Initialize MongoDB clients for rules and data
        mongo_client = MongoClient(os.environ.get("MONGO_URI"))  # Replace with your MongoDB connection string
        rules_service = BaseMongoService(mongo_client, rules_collection_name)
        data_service = BaseMongoService(mongo_client, dataCollectionName)

        # Fetch all rules from the rules collection
        rules = rules_service.get_all()

        # Initialize the response dictionary
        violations = {}

        # Iterate through each rule and execute the associated query
        for rule in rules:
            field_name = rule.get("fieldName")
            query = rule.get("query")
            rule_description = rule.get("rule")

            if not query:
                continue  # Skip if no query is defined for the rule

            # Run the query against the data collection
            try:
                query_dict = eval(query)  # Convert the query string to a dictionary
                records = data_service.get_all(query=query_dict)

                # Process each record and group violations
                for record in records:
                    row_number = record.get("row_number")
                    if row_number not in violations:
                        violations[row_number] = {
                            "row_number": row_number,
                            "rules_violated": [],
                            "associated_columns": [],
                            "remediation": []
                        }
                    violations[row_number]["rules_violated"].append(rule_description)
                    violations[row_number]["associated_columns"].append(field_name)
            except Exception as e:
                print(f"Error executing query for field '{field_name}': {e}")

        # Convert violations dictionary to a list
        violations_list = list(violations.values())
        print(len(violations_list))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch violations: {str(e)}")

    return dto(isSuccess=True, data=violations_list)