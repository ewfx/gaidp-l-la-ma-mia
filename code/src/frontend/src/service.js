import axios from "axios";

// Create an Axios instance
const api = axios.create({
  baseURL: "http://localhost:8000", // Replace with your API base URL
  headers: {
    "Content-Type": "application/json",
  },
});

// Function to handle GET requests
export const getData = async () => {
  try {
    const response = await api.get("/file/list");
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
        Name: "samplePdf1.pdf",
        Schedules: [
          {
            Name: "schedule1",
            Categories: [
              { Name: "AFS Auto", page: 1 },
              { Name: "Car Loan", page: 2 },
              { Name: "LIQ", page: 3 },
            ],
          },
          {
            Name: "schedule2",
            Categories: [
              { Name: "AFS Auto2", page: 1 },
              { Name: "Car Loan2", page: 2 },
              { Name: "LIQ2", page: 3 },
            ],
          },
        ],
      },
      {
        Name: "samplePdf2.pdf",
        Schedules: [
          {
            Name: "schedule2",
            Categories: [
              { Name: "AFS Auto", page: 1 },
              { Name: "Car Loan", page: 2 },
              { Name: "LIQ", page: 3 },
            ],
          },
          {
            Name: "schedule3",
            Categories: [
              { Name: "AFS Auto2", page: 1 },
              { Name: "Car Loan2", page: 2 },
              { Name: "LIQ2", page: 3 },
            ],
          },
        ],
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
