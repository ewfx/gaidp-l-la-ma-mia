import React, { useState, useEffect } from "react";
import axios from "axios";
import SelectorComponent from "../../components/SelectorComponent.jsx";
import ChatComponent from "../../components/ChatComponent.jsx";
import DataTableComponent from "../../components/DataTableComponent.jsx";
import ProfilingRuleTableComponent from "../../components/ProfilingRuleTableComponent.jsx";
import { Button, Snackbar, Alert } from "@mui/material";

function ProfilingRulesComponent() {
  const [categories, setCategories] = useState([]);
  const [selectedPdf, setSelectedPdf] = useState("PDFName"); // Default value for selectedPdf
  const [selectedSchedule, setSelectedSchedule] = useState("ScheduleA"); // Default value for selectedSchedule
  const [selectedSection, setSelectedSection] = useState("USAutoLoan"); // Default value for selectedSection
  const [profiledData, setProfiledData] = useState([]);
  const [profilingRuleData, setProfilingRuleData] = useState([]);
  const [csvFile, setCsvFile] = useState(null); // State to store the selected CSV file
  const [snackbarOpen, setSnackbarOpen] = useState(false); // State for Snackbar visibility
  const [snackbarMessage, setSnackbarMessage] = useState(""); // State for Snackbar message
  const [snackbarSeverity, setSnackbarSeverity] = useState("success"); // State for Snackbar severity

  // Fetch categories on component mount
  useEffect(() => {
    getCategoryData().then((data) => {
      setCategories(data);
    });
  }, []);

  // Fetch profiling rules whenever pdf, schedule, or section changes
  useEffect(() => {
    if (selectedPdf && selectedSchedule && selectedSection) {
      fetchProfilingRules(selectedPdf, selectedSchedule, selectedSection);
    }
  }, [selectedPdf, selectedSchedule, selectedSection]);

  const getCategoryData = async () => {
    // Mocked API call to fetch categories
    return [
      {
        Name: "PDFName",
        Schedules: [
          {
            Name: "ScheduleA",
            Categories: [{ Name: "USAutoLoan" }, { Name: "END" }],
          },
        ],
      },
    ];
  };

  const fetchProfilingRules = async (pdf, schedule, category) => {
    try {
      console.log("Fetching profiling rules...");
      const response = await axios.get(
        `http://127.0.0.1:8000/rule?pdf=${pdf}&schedule=${schedule}&category=${category}`
      );
      console.log("Profiling rules response:", response.data);
      if (response.data.isSuccess) {
        setProfilingRuleData(response.data.data);
      } else {
        console.error("Error fetching profiling rules:", response.data.errorMessage);
      }
    } catch (error) {
      console.error("Error fetching profiling rules:", error);
    }
  };

  const handleCsvUpload = async () => {
    if (!csvFile) {
      alert("Please select a CSV file to upload.");
      return;
    }

    const formData = new FormData();
    formData.append("file", csvFile);

    try {
      const response = await axios.post("http://127.0.0.1:8000/data/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      console.log("CSV upload response:", response.data);

      // Show success popup
      setSnackbarMessage("CSV file uploaded successfully!");
      setSnackbarSeverity("success");
      setSnackbarOpen(true);
    } catch (error) {
      console.error("Error uploading CSV file:", error);

      // Show error popup
      setSnackbarMessage("Failed to upload CSV file.");
      setSnackbarSeverity("error");
      setSnackbarOpen(true);
    }
  };

  const handleFileChange = (event) => {
    setCsvFile(event.target.files[0]);
  };

  const handleSnackbarClose = () => {
    setSnackbarOpen(false);
  };

  const handlePdfChange = (event) => {
    setSelectedPdf(event.target.value);
    setSelectedSchedule("");
    setSelectedSection("");
  };

  const handleScheduleChange = (event) => {
    setSelectedSchedule(event.target.value);
    setSelectedSection("");
  };

  const handleSectionChange = (event) => {
    setSelectedSection(event.target.value);
  };

  const getSchedules = () => {
    const pdf = categories.find((item) => item.Name === selectedPdf);
    return pdf ? pdf.Schedules : [];
  };

  const getSections = () => {
    const schedules = getSchedules();
    const schedule = schedules.find((item) => item.Name === selectedSchedule);
    return schedule
      ? schedule["Categories"]
          .filter((x) => x.Name !== "END")
          .map((x) => x.Name)
      : [];
  };

  return (
    <div
      style={{
        height: "calc(100vh - 64px)",
        width: "100%",
        display: "flex",
        flexDirection: "row",
      }}
    >
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          height: "100%",
          width: "70%",
          overflow: "auto",
        }}
      >
        <SelectorComponent
          categories={categories}
          selectedPdf={selectedPdf}
          handlePdfChange={handlePdfChange}
          selectedSchedule={selectedSchedule}
          handleScheduleChange={handleScheduleChange}
          getSchedules={getSchedules}
          selectedSection={selectedSection}
          handleSectionChange={handleSectionChange}
          getSections={getSections}
        />
        <ProfilingRuleTableComponent profilingRuleData={profilingRuleData} />
        <div style={{ display: "flex", alignItems: "center", gap: "16px", marginTop: "16px" }}>
          <DataTableComponent profiledData={profiledData} />
          <div>
            <input type="file" accept=".csv" onChange={handleFileChange} />
            <Button
              variant="contained"
              color="primary"
              onClick={handleCsvUpload}
              style={{ marginTop: "8px" }}
            >
              Upload CSV
            </Button>
          </div>
        </div>
      </div>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          height: "100%",
          width: "30%",
          backgroundColor: "#24222F",
        }}
      >
        <ChatComponent />
      </div>

      {/* Snackbar for upload notifications */}
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={3000}
        onClose={handleSnackbarClose}
        anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
      >
        <Alert onClose={handleSnackbarClose} severity={snackbarSeverity} sx={{ width: "100%" }}>
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </div>
  );
}

export default ProfilingRulesComponent;
