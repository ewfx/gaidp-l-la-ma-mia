import React, { useState, useEffect } from "react";
import { getData } from "../../service.js";
import SelectorComponent from "../../components/SelectorComponent.jsx";

function ProfilingRulesComponent() {
  const [categories, setCategories] = useState([]);
  const [selectedPdf, setSelectedPdf] = useState("");
  const [selectedSchedule, setSelectedSchedule] = useState("");
  const [selectedSection, setSelectedSection] = useState("");

  useEffect(() => {
    getData().then((data) => {
      setCategories(data);
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
    const pdf = categories.find((item) => item.Name === selectedPdf);
    return pdf ? pdf.Schedules : [];
  };

  const getSections = () => {
    const schedules = getSchedules();
    const schedule = schedules.find((item) => item.Name === selectedSchedule);
    return schedule
      ? schedule["Categories"]
          .filter((x) => {
            return x.Name !== "END";
          })
          .map((x) => {
            return x.Name;
          })
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
          width: "65%",
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
      </div>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          height: "100%",
          width: "35%",
          backgroundColor: "black",
        }}
      ></div>
    </div>
  );
}

export default ProfilingRulesComponent;
