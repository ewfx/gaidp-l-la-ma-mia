import React, { useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
  Collapse,
} from "@mui/material";

function ProfilingRuleTableComponent({ profilingRuleData }) {
  const [open, setOpen] = useState(true);

  return (
    <div style={{ textAlign: "center", marginTop: "20px" }}>
      <Button
        variant="contained"
        color="primary"
        onClick={() => setOpen(!open)}
        sx={{ marginBottom: "20px" }}
      >
        {open ? "Hide Profiling Rules" : "Show Profiling Rules"}
      </Button>

      <Collapse in={open}>
        <TableContainer
          component={Paper}
          sx={{
            width: "80%",
            border: "1px solid #ccc",
            alignSelf: "center",
            margin: "auto",
          }}
        >
          <Table sx={{ minWidth: 650 }} aria-label="collapsible table">
            <TableHead sx={{ backgroundColor: "#DD1E25", color: "white" }}>
              <TableRow>
                <TableCell
                  sx={{ border: "1px solid #ddd", color: "white" }}
                  align="left"
                >
                  Associated Column
                </TableCell>
                <TableCell
                  sx={{ border: "1px solid #ddd", color: "white" }}
                  align="left"
                >
                  Profiling Rule
                </TableCell>
                <TableCell
                  sx={{ border: "1px solid #ddd", color: "white" }}
                  align="left"
                >
                  Page No.
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {profilingRuleData.map((row) => (
                <TableRow key={row._id + row.rule}>
                  <TableCell sx={{ border: "1px solid #ddd" }} align="left">
                    {row.columnName}
                  </TableCell>
                  <TableCell sx={{ border: "1px solid #ddd" }} align="left">
                    {row.rule}
                  </TableCell>
                  <TableCell sx={{ border: "1px solid #ddd" }} align="left">
                    {row.page}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Collapse>
    </div>
  );
}

export default ProfilingRuleTableComponent;
