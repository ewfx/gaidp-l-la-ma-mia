import React, { useState, useEffect } from "react";
import axios from "axios";
import SelectorComponent from "../../components/SelectorComponent.jsx";
import ChatComponent from "../../components/ChatComponent.jsx";
import DataTableComponent from "../../components/DataTableComponent.jsx";
import ProfilingRuleTableComponent from "../../components/ProfilingRuleTableComponent.jsx";
import { Button, Snackbar, Alert, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle } from "@mui/material";

function ProfilingRulesComponent() {
  const [categories, setCategories] = useState([]);
  const [selectedPdf, setSelectedPdf] = useState(null); // Default value for selectedPdf
  const [selectedSchedule, setSelectedSchedule] = useState(""); // Default value for selectedSchedule
  const [selectedCategory, setSelectedCategory] = useState(""); // Default value for selectedSection
  const [dataCollectionName, setDataCollectionName] = useState();
  const [violations, setViolations] = useState();
  const [profilingRuleData, setProfilingRuleData] = useState();
  const [csvFile, setCsvFile] = useState(null); // State to store the selected CSV file
  const [snackbarOpen, setSnackbarOpen] = useState(false); // State for Snackbar visibility
  const [snackbarMessage, setSnackbarMessage] = useState(""); // State for Snackbar message
  const [snackbarSeverity, setSnackbarSeverity] = useState("success"); // State for Snackbar severity
  const [generateDialogOpen, setGenerateDialogOpen] = useState(false);

  // Fetch categories on component mount
  useEffect(() => {
    getCategoryData().then((data) => {
      setCategories(data);
    });
  }, []);

  // Fetch profiling rules whenever pdf, schedule, or section changes
  useEffect(() => {
    if (selectedPdf && selectedSchedule && selectedCategory) {
      checkIfRulesExist(selectedPdf, selectedSchedule, selectedCategory)
    }
  }, [selectedPdf, selectedSchedule, selectedCategory]);

  const checkIfRulesExist = async (pdf, schedule, category) => {
    try {
      console.log("Checking if profiling rules exist");
      axios.get(`http://127.0.0.1:8000/data/isrulesavailbale?pdfName=${pdf}&schedule=${schedule}&category=${category}`)
      .then((response) => {
        if (response.data.isSuccess) {
          console.log("Rules exist:", response.data.data.exists);
          if(response.data.data.exists) {
            fetchProfilingRules(selectedPdf, selectedSchedule, selectedCategory);
          } else {
            console.log("dfhjdksf")
            setGenerateDialogOpen(true); // Open dialog if rules don't exist
          }
        } else {
          console.error("Error checking for rules");
        }
    })
    } catch (error) {
      console.error("Error checkinf if rules exist:", error);
    }
  }

  const getCategoryData = async () => {
    try {
      console.log("Fetching profiling rules...");
      const response = await axios.get(`http://127.0.0.1:8000/file/list`);
      console.log("Index response:", response.data);
      if (response.data.isSuccess) {
        return response.data.data;
      } else {
        console.error("Error fetching index:", response.data.errorMessage);
      }
    } catch (error) {
      console.error("Error fetching index:", error);
    }
  };

  const fetchProfilingRules = async (pdf, schedule, category) => {
    try {
      console.log("Fetching profiling rules...");
      const response = await axios
        .get(
          `http://127.0.0.1:8000/rule?pdfName=${pdf}&schedule=${schedule}&category=${category}`
        )
        .then((response) => {
          console.log("Profiling rules response:", response.data);
          if (response.data.isSuccess) {
            setProfilingRuleData(response.data.data);
          } else {
            console.error(
              "Error fetching profiling rules:",
              response.data.errorMessage
            );
          }
        });
    } catch (error) {
      console.error("Error fetching profiling rules:", error);
    }
  };

  const handleGenerateRules = async () => {
    if (!(selectedPdf && selectedSchedule && selectedCategory)) {
      setSnackbarMessage("Please select PDF, Schedule, and Section.");
      setSnackbarSeverity("error");
      setSnackbarOpen(true);
      return;
    }

    setSnackbarMessage("Generating rules...");
    setSnackbarSeverity("info");
    setSnackbarOpen(true);

    try {
      const response = await axios.post(
        `http://localhost:8000/data/extractprofilingrules?pdfName=${selectedPdf}&schedule=${selectedSchedule}&category=${selectedCategory}`
      );

      if (response.status === 200) {
        setSnackbarMessage("Rules generated successfully!");
        setSnackbarSeverity("success");
        setSnackbarOpen(true);
        fetchProfilingRules(selectedPdf, selectedSchedule, selectedCategory); // Refresh the profiling rules
      } else {
        setSnackbarMessage("Failed to generate rules.");
        setSnackbarSeverity("error");
        setSnackbarOpen(true);
      }
    } catch (error) {
      console.error("Error generating rules:", error);
      setSnackbarMessage("Error generating rules.");
      setSnackbarSeverity("error");
      setSnackbarOpen(true);
    }
  };

  const handleGenerateRulesConfirm = async () => {
    setGenerateDialogOpen(false);
    setSnackbarMessage("Generating rules...");
    setSnackbarSeverity("info");
    setSnackbarOpen(true);

    try {
      const response = axios.post(
        `http://localhost:8000/data/extractprofilingrules?pdfName=${selectedPdf}&schedule=${selectedSchedule}&category=${selectedCategory}`
      );

      // if (response.status === 200) {
      //   setSnackbarMessage("Rules generated successfully!");
      //   setSnackbarSeverity("success");
      //   setSnackbarOpen(true);
      //   fetchProfilingRules(selectedPdf, selectedSchedule, selectedCategory); // Refresh the profiling rules
      // } else {
      //   setSnackbarMessage("Failed to generate rules.");
      //   setSnackbarSeverity("error");
      //   setSnackbarOpen(true);
      // }
    } catch (error) {
      console.error("Error generating rules:", error);
      setSnackbarMessage("Error generating rules.");
      setSnackbarSeverity("error");
      setSnackbarOpen(true);
    }
  };

  const handleGenerateRulesCancel = () => {
    setGenerateDialogOpen(false);
  };

  const fetchViolations = async (
    pdf,
    schedule,
    category,
    dataCollectionName
  ) => {
    try {
      console.log("Fetching profiling rules...");
      const response = await axios
        .get(
          `http://127.0.0.1:8000/data/violations?pdfName=${pdf}&schedule=${schedule}&category=${category}&dataCollectionName=${dataCollectionName}`
        )
        .then((response) => {
          console.log("Violations response:", response.data);
          if (response.data.isSuccess) {
            setViolations(response.data.data);
          } else {
            console.error(
              "Error fetching violations:",
              response.data.errorMessage
            );
          }
        });
    } catch (error) {
      console.error("Error fetching profiling rules:", error);
    }
  };

  const handleCsvUpload = async () => {
    if (!csvFile) {
      alert("Please select a CSV file to upload.");
      return;
    }

    if (!(selectedPdf && selectedSchedule && selectedCategory)) {
      // Show error popup
      setSnackbarMessage("Please select PDF, Schedule, and Section.");
      setSnackbarSeverity("error");
      setSnackbarOpen(true);
      return;
    }

    const formData = new FormData();
    formData.append("file", csvFile);

    try {
      const response = await axios.post(
        `http://127.0.0.1:8000/data/uploadcsv?pdfName=${selectedPdf}&schedule=${selectedSchedule}&category=${selectedCategory}`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      if (response.data.isSuccess) {
        console.log("CSV upload response:", response.data);
        setDataCollectionName(response.data.data.collection_name);
        fetchViolations(
          selectedPdf,
          selectedSchedule,
          selectedCategory,
          response.data.data.collection_name
        );
      }

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

  const handlePdfUpload = async () => {
    if (!selectedPdf) {
      setSnackbarMessage("Please select PDF file to upload.");
      setSnackbarSeverity("error");
      setSnackbarOpen(true);
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedPdf);

    try {
      const response = await axios.post(
        `http://127.0.0.1:8000/data/uploadpdf`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      if (response.data.isSuccess) {
        console.log("PDF upload response:", response.data);
        getCategoryData().then((data) => {
          setCategories(data);
        });
      }

      // Show success popup
      setSnackbarMessage("PDF file uploaded successfully!");
      setSnackbarSeverity("success");
      setSnackbarOpen(true);
    } catch (error) {
      console.error("Error uploading PDF file:", error);

      // Show error popup
      setSnackbarMessage("Failed to upload PDF file.");
      setSnackbarSeverity("error");
      setSnackbarOpen(true);
    }
  };

  const handleFileChange = (event) => {
    setCsvFile(event.target.files[0]);
  };

  const handlePdfUploadChange = (event) => {
    setSelectedPdf(event.target.files[0]);
  };

  const handleSnackbarClose = () => {
    setSnackbarOpen(false);
  };

  const handlePdfChange = (event) => {
    setSelectedPdf(event.target.value);
    setSelectedSchedule("");
    setSelectedCategory("");
  };

  const handleScheduleChange = (event) => {
    setSelectedSchedule(event.target.value);
    setSelectedCategory("");
  };

  const handleSectionChange = (event) => {
    setSelectedCategory(event.target.value);
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
        overflow: "hidden", // Prevent scrolling for the entire page
      }}
    >
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          height: "100%",
          width: "70%",
          overflow: "auto", // Enable scrolling only for this section
        }}
      >
        {/* PDF Upload Section */}
        <div
          style={{
            display: "flex",
            flexDirection: "row",
            alignItems: "center",
            justifyContent: "center",
            width: "100%",
            marginTop: "35px",
            marginBottom: "0px",
          }}
        >
          <div style={{ textAlign: "center" }}>
            <input type="file" accept=".pdf" onChange={handlePdfUploadChange} />
            <Button
              variant="contained"
              color="primary"
              onClick={handlePdfUpload}
              style={{ marginTop: "8px" }}
            >
              Upload PDF
            </Button>
          </div>
        </div>
        {/* end */}
        <SelectorComponent
          categories={categories}
          selectedPdf={selectedPdf}
          handlePdfChange={handlePdfChange}
          selectedSchedule={selectedSchedule}
          handleScheduleChange={handleScheduleChange}
          getSchedules={getSchedules}
          selectedSection={selectedCategory}
          handleSectionChange={handleSectionChange}
          getSections={getSections}
        />
        {profilingRuleData ? (
          <ProfilingRuleTableComponent profilingRuleData={profilingRuleData} />
        ) : (
          <></>
        )}
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            height: "100%",
          }}
        >
          <div style={{ textAlign: "center" }}>
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
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "16px",
            marginTop: "16px",
          }}
        >
          {violations ? <DataTableComponent violations={violations} /> : <></>}
        </div>
      </div>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          height: "calc(100vh - 64px)",
          width: "30%",
          backgroundColor: "#24222F",
          overflow: "auto", // Ensure scrolling is handled here if needed
        }}
      >
        <ChatComponent
          pdfName={selectedPdf}
          schedule={selectedSchedule}
          category={selectedCategory}
          fetchProfilingRules={fetchProfilingRules}
          dataCollectionName={dataCollectionName}
          fetchViolations={fetchViolations}
          profilingRuleData={profilingRuleData}
        />
      </div>

      {/* Snackbar for upload notifications */}
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={3000}
        onClose={handleSnackbarClose}
        anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
      >
        <Alert
          onClose={handleSnackbarClose}
          severity={snackbarSeverity}
          sx={{ width: "100%" }}
        >
          {snackbarMessage}
        </Alert>
      </Snackbar>

      <Dialog
        open={generateDialogOpen}
        onClose={handleGenerateRulesCancel}
        aria-labelledby="generate-dialog-title"
        aria-describedby="generate-dialog-description"
      >
        <DialogTitle id="generate-dialog-title">Generate Rules</DialogTitle>
        <DialogContent>
          <DialogContentText id="generate-dialog-description">
            Profiling rules for the selected category do not exist. Would you like to generate them?
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleGenerateRulesCancel} color="secondary">
            Cancel
          </Button>
          <Button onClick={handleGenerateRulesConfirm} color="primary" autoFocus>
            Confirm
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}

export default ProfilingRulesComponent;
