import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from services.anomaly_detection import detect_anomalies
import shutil
from dto.response_dto import ResponseDTO as dto

router = APIRouter(prefix="/anomaly", tags=["Anomaly Detection"])

@router.post("/detect")
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
    temp_file_path = f"/tmp/{file.filename}"
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