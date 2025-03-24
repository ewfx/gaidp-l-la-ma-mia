import axios from "axios";

// Create an Axios instance
const api = axios.create({
  baseURL: "http://localhost:8000", // Replace with your API base URL
  headers: {
    "Content-Type": "application/json",
  },
});

// Function to handle GET requests
export const getCategoryData = async () => {
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

//Function to get Profiled Data Component info
export const getProfiledData = async () => {
  try {
    const response = await api.get("/file/getProfiledDate");
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
        remediation: "change it to current or past",
      },
      {
        id: "002",
        profilingRuleViolated: "balance has special characters",
        column: "balance",
        remediation: "update field to be numeric ",
      },
    ];
  }
};

//Function to get Profiling Rules Data
export const getProfilingRules = async () => {
  let data = [];
  try {
    const response = await api.get("/file/getProfiledDate");
    let data = [];
    if (response && response.data && response.data.isSuccess) {
      if (response.data.data.length() !== 0) data = response.data.data;
    } else {
      //throw new Error("Error fetching data");
    }
  } catch (error) {
    console.error("Error fetching data:", error);
    //throw error;
    //dummy data being returned if api is not up
    data = [
      {
        _id: "67dfbf1250b7ef3de85d4d11",
        columnName: "email",
        description: "User's email address",
        rules: [
          {
            rule: "Email must be in valid format",
            query:
              "{ email: { $not: { $regex: '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$' } } }",
            page: 1,
          },
          {
            rule: "Email must be unique across all records",
            query:
              "{ $group: { _id: '$email', count: { $sum: 1 } }, $having: { count: { $gt: 1 } } }",
            page: 2,
          },
        ],
      },
      {
        _id: "67dfbf1250b7ef3de85d4d12",
        columnName: "phoneNumber",
        description: "Contact phone number",
        rules: [
          {
            rule: "Phone number must be 10 digits long",
            query: "{ phoneNumber: { $not: { $regex: '^\\d{10}$' } } }",
            page: 3,
          },
          {
            rule: "Phone number must not be empty if required",
            query: "{ phoneNumber: { $exists: true, $eq: '' } }",
            page: 4,
          },
        ],
      },
      {
        _id: "67dfbf1250b7ef3de85d4d13",
        columnName: "orderStatus",
        description: "Current status of the order",
        rules: [
          {
            rule: "Status must be one of: pending, processing, shipped, delivered, cancelled",
            query:
              "{ orderStatus: { $nin: ['pending', 'processing', 'shipped', 'delivered', 'cancelled'] } }",
            page: 6,
          },
        ],
      },
    ];
  }
  //now we have data
  let profilingRuleData = [];
  data.forEach((element) => {
    let rules = element.rules;
    rules.forEach((rule) => {
      profilingRuleData.push({
        _id: element._id,
        columnName: element.columnName,
        rule: rule.rule,
        page: rule.page,
      });
    });
  });
  return profilingRuleData;
};

// Function to handle POST requests
export const getChatQueryResponse = async (query) => {
  try {
    const response = await api.post("/chat/getResponse", query);
    return response.data;
  } catch (error) {
    console.error("Error posting data:", error);
    //throw error;
    return "Error fetching response";
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
