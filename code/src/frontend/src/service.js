import axios from "axios";

// Create an Axios instance
const api = axios.create({
  baseURL: "http://localhost:8000", // Replace with your API base URL
  headers: {
    "Content-Type": "application/json",
  },
});

// Function to handle GET requests
export const getData = async (endpoint) => {
  try {
    const response = await api.get(endpoint);
    if (response && response.data && response.data.isSuccess) {
      return response.data.data;
    } else {
      throw new Error("Error fetching data");
    }
  } catch (error) {
    console.error("Error fetching data:", error);
    //throw error;
    //dummy data being returned if api is not up
    return [
      {
        pdfName: "samplePdf1.pdf",
        schedules: [
          {
            scheduleName: "schedule1",
            sections: ["AFS Auto", "Car Loan", "LIQ"],
          },
          {
            scheduleName: "schedule2",
            sections: ["AFS Auto2", "Car Loan2", "LIQ2"],
          },
        ],
      },
      {
        pdfName: "samplePdf2.pdf",
        schedules: [
          {
            scheduleName: "schedule2",
            sections: ["Commercial Loan", "Car Loan", "LIQ"],
          },
          {
            scheduleName: "schedule3",
            sections: ["AFS Auto3", "LIQ3"],
          },
        ],
      },
    ];
  }
};

//Function to get Profiled Data Component info
export const getProfiledData = async (endpoint) => {
  try {
    const response = await api.get(endpoint);
    if (response && response.data && response.data.isSuccess) {
      return response.data.data;
    } else {
      throw new Error("Error fetching data");
    }
  } catch (error) {
    console.error("Error fetching data:", error);
    //throw error;
    //dummy data being returned if api is not up
    return [
      {
        id: "001",
        profilingRuleViolated: "Data is future",
        column: "date",
        remediation: "change it to current or past"
      },
      {
        id: "002",
        profilingRuleViolated: "balance has special characters",
        column: "balance",
        remediation: "update field to be numeric "
      },
    ];
  }
};

// Function to handle POST requests
export const postData = async (endpoint, data) => {
  try {
    const response = await api.post(endpoint, data);
    return response.data;
  } catch (error) {
    console.error("Error posting data:", error);
    throw error;
  }
};

// Function to handle PUT requests
export const putData = async (endpoint, data) => {
  try {
    const response = await api.put(endpoint, data);
    return response.data;
  } catch (error) {
    console.error("Error updating data:", error);
    throw error;
  }
};

// Function to handle DELETE requests
export const deleteData = async (endpoint) => {
  try {
    const response = await api.delete(endpoint);
    return response.data;
  } catch (error) {
    console.error("Error deleting data:", error);
    throw error;
  }
};
