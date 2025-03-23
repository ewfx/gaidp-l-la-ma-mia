import { Box, FormControl, InputLabel, MenuItem, Select } from "@mui/material";
function SelectorComponent({
  categories,
  selectedPdf,
  handlePdfChange,
  selectedSchedule,
  handleScheduleChange,
  getSchedules,
  selectedSection,
  handleSectionChange,
  getSections,
}) {
  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: "flex-start",
        gap: 2,
        marginTop: "20px",
        marginLeft: "20px",
      }}
    >
      <FormControl variant="outlined" sx={{ minWidth: 200 }}>
        <InputLabel>PDF Name</InputLabel>
        <Select value={selectedPdf} onChange={handlePdfChange} label="PDF Name">
          {categories.map((category) => (
            <MenuItem key={category.pdfName} value={category.pdfName}>
              {category.pdfName}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <FormControl
        variant="outlined"
        sx={{ minWidth: 200 }}
        disabled={!selectedPdf}
      >
        <InputLabel>Schedule</InputLabel>
        <Select
          value={selectedSchedule}
          onChange={handleScheduleChange}
          label="Schedule"
        >
          {getSchedules().map((schedule) => (
            <MenuItem key={schedule.scheduleName} value={schedule.scheduleName}>
              {schedule.scheduleName}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <FormControl
        variant="outlined"
        sx={{ minWidth: 200 }}
        disabled={!selectedSchedule}
      >
        <InputLabel>Section</InputLabel>
        <Select
          value={selectedSection}
          onChange={handleSectionChange}
          label="Section"
        >
          {getSections().map((section, index) => (
            <MenuItem key={index} value={section}>
              {section}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
    </Box>
  );
}

export default SelectorComponent;
