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
      <FormControl variant="outlined" sx={{ minWidth: 250, maxWidth: 250 }}>
        <InputLabel>PDF Name</InputLabel>
        <Select value={selectedPdf} onChange={handlePdfChange} label="PDF Name">
          {categories.map((category) => (
            <MenuItem key={category.Name} value={category.Name}>
              {category.Name}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <FormControl
        variant="outlined"
        sx={{ minWidth: 250, maxWidth: 250 }}
        disabled={!selectedPdf}
      >
        <InputLabel>Schedule</InputLabel>
        <Select
          value={selectedSchedule}
          onChange={handleScheduleChange}
          label="Schedule"
        >
          {getSchedules().map((schedule) => (
            <MenuItem key={schedule.Name} value={schedule.Name}>
              {schedule.Name}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <FormControl
        variant="outlined"
        sx={{ minWidth: 250, maxWidth: 250 }}
        disabled={!selectedSchedule}
      >
        <InputLabel>Category</InputLabel>
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
