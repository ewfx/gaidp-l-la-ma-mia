import React, { useState, useEffect } from "react";
import { getCategoryData, getProfiledData } from "../../service.js";
import SelectorComponent from "../../components/SelectorComponent.jsx";
import DataTableComponent from "../../components/DataTableComponent.jsx";

function DataComponent() {
  const [categories, setCategories] = useState([]);
  const [selectedPdf, setSelectedPdf] = useState("");
  const [selectedSchedule, setSelectedSchedule] = useState("");
  const [selectedSection, setSelectedSection] = useState("");
  const [profiledData, setProfiledData] = useState([]);

  useEffect(() => {
    getCategoryData().then((data) => {
      setCategories(data);
    });
  }, []);

  // Set Profiled Data

  useEffect(() => {
    getProfiledData().then((data) => {
      setProfiledData(data);
    });
  }, []);

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
    const pdf = categories.find((item) => item.pdfName === selectedPdf);
    return pdf ? pdf.schedules : [];
  };

  const getSections = () => {
    const schedules = getSchedules();
    const schedule = schedules.find(
      (item) => item.scheduleName === selectedSchedule
    );
    return schedule ? schedule.sections : [];
  };

  return (
    <div>
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
      <br />
      <DataTableComponent profiledData={profiledData} />
    </div>
  );
}

export default DataComponent;
