import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from services.anomaly_detection import detect_anomalies
import shutil
from dto.response_dto import ResponseDTO as dto
from datetime import datetime

router = APIRouter(prefix="/data", tags=["Anomaly Detection"])

@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
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

    return dto(isSuccess=True, data={"filename": filename})

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