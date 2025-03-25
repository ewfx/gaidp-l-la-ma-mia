import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from services.anomaly_detection import detect_anomalies
from services.base_mongo_service import BaseMongoService  # Import BaseMongoService
import shutil
from dto.response_dto import ResponseDTO as dto
from datetime import datetime
import pandas as pd
import uuid
from pymongo import MongoClient

router = APIRouter(prefix="/data", tags=["Anomaly Detection"])

@router.post("/upload")
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

        # Generate a unique collection name
        collection_name = f"{pdfName}_{schedule}_{category}_{uuid.uuid4().hex}"

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