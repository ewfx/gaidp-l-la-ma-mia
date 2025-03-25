# Backend

This guide explains how to set up and run a FastAPI application on `localhost:8000`.

## Prerequisites

- Python 3.12+ installed
- `pip` (Python package manager) installed
- `uvicorn` for running the FastAPI server

## Step 1: Create a Virtual Environment (Optional but Recommended)

Run the following commands:

```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

## Run the app

```
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```