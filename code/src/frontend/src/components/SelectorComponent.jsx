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
        justifyContent: "center",
        gap: 2,
        marginTop: "30px",
        marginLeft: "30px",
      }}
    >
      <FormControl variant="outlined" sx={{ minWidth: 300, maxWidth: 300 }}>
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
        sx={{ minWidth: 200, maxWidth: 200 }}
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
        sx={{ minWidth: 350, maxWidth: 350 }}
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
