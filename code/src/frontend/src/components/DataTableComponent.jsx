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

function DataTableComponent({ profiledData }) {
  const [open, setOpen] = useState(true);

  return (
    <div
      style={{ textAlign: "center", marginTop: "20px", marginBottom: "30px" }}
    >
      <Button
        variant="contained"
        color="primary"
        onClick={() => setOpen(!open)}
        sx={{ marginBottom: "20px" }}
      >
        {open ? "Hide Data" : "Show Data"}
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
                  Data ID
                </TableCell>
                <TableCell
                  sx={{ border: "1px solid #ddd", color: "white" }}
                  align="left"
                >
                  Profiling Rule Violated
                </TableCell>
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
                  Remediation
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {profiledData.map((row) => (
                <TableRow key={row.id}>
                  <TableCell sx={{ border: "1px solid #ddd" }} align="left">
                    {row.id}
                  </TableCell>
                  <TableCell sx={{ border: "1px solid #ddd" }} align="left">
                    {row.profilingRuleViolated}
                  </TableCell>
                  <TableCell sx={{ border: "1px solid #ddd" }} align="left">
                    {row.column}
                  </TableCell>
                  <TableCell sx={{ border: "1px solid #ddd" }} align="left">
                    {row.remediation}
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

export default DataTableComponent;
