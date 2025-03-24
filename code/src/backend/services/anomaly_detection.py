import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(csv_file, contamination=0.01, random_state=42):
    """
    Detects anomalies in a CSV file using the Isolation Forest algorithm.

    Args:
        csv_file (str): Path to the CSV file.
        contamination (float): The proportion of anomalies in the data (default is 0.05).
        random_state (int): Random state for reproducibility (default is 42).

    Returns:
        list: A list of row numbers (0-indexed) that are identified as anomalies.
    """
    # Load the CSV file into a DataFrame
    try:
        data = pd.read_csv(csv_file)
    except FileNotFoundError:
        raise Exception(f"File not found: {csv_file}")
    except pd.errors.EmptyDataError:
        raise Exception("The provided CSV file is empty.")
    except pd.errors.ParserError:
        raise Exception("Error parsing the CSV file.")

    # Preprocess the data
    # Separate numeric and non-numeric columns
    numeric_data = data.select_dtypes(include=["number"])
    categorical_data = data.select_dtypes(exclude=["number"])

    # One-hot encode categorical data
    if not categorical_data.empty:
        categorical_data = pd.get_dummies(categorical_data, drop_first=True)

    # Combine numeric and encoded categorical data
    if not numeric_data.empty and not categorical_data.empty:
        processed_data = pd.concat([numeric_data, categorical_data], axis=1)
    elif not numeric_data.empty:
        processed_data = numeric_data
    elif not categorical_data.empty:
        processed_data = categorical_data
    else:
        raise Exception("The CSV file does not contain any usable data.")

    # Initialize the Isolation Forest model
    model = IsolationForest(contamination=contamination, random_state=random_state)

    # Fit the model and predict anomalies
    model.fit(processed_data)
    predictions = model.predict(processed_data)

    # Identify anomalies (predictions == -1)
    anomalies = [index for index, prediction in enumerate(predictions) if prediction == -1]

    return anomalies

# Example usage
if __name__ == "__main__":
    csv_path = "/Users/parthshukla/Documents/_working_space/gaidp-l-la-ma-mia/code/src/backend/data/autogen_data_usautoloans.csv"  # Replace with the path to your CSV file
    anomalies = detect_anomalies(csv_path)
    print(f"Anomalies found at row numbers: {anomalies}")