import React, { useState, useEffect } from "react";
import {
  getCategoryData,
  getProfiledData,
  getProfilingRules,
} from "../../service.js";
import SelectorComponent from "../../components/SelectorComponent.jsx";
import ChatComponent from "../../components/ChatComponent.jsx";
import DataTableComponent from "../../components/DataTableComponent.jsx";
import ProfilingRuleTableComponent from "../../components/ProfilingRuleTableComponent.jsx";

function ProfilingRulesComponent() {
  const [categories, setCategories] = useState([]);
  const [selectedPdf, setSelectedPdf] = useState("");
  const [selectedSchedule, setSelectedSchedule] = useState("");
  const [selectedSection, setSelectedSection] = useState("");
  const [profiledData, setProfiledData] = useState([]);
  const [profilingRuleData, setProfilingRuleData] = useState([]);

  useEffect(() => {
    getCategoryData().then((data) => {
      setCategories(data);
    });
    getProfiledData().then((data) => {
      setProfiledData(data);
    });
    getProfilingRules().then((data) => {
      console.log(data);
      setProfilingRuleData(data);
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
        <DataTableComponent profiledData={profiledData} />
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
    </div>
  );
}

export default ProfilingRulesComponent;
