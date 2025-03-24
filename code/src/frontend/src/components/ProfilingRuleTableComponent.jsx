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
                  Description
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
                  Query
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {profilingRuleData.map((row) => (
                <TableRow key={row.columnName}>
                  <TableCell sx={{ border: "1px solid #ddd" }} align="left">
                    {row.columnName}
                  </TableCell>
                  <TableCell sx={{ border: "1px solid #ddd" }} align="left">
                    {row.description}
                  </TableCell>
                  <TableCell sx={{ border: "1px solid #ddd" }} align="left">
                    {row.rules.map((ruleObj, index) => (
                      <div key={index}>{ruleObj.rule}</div>
                    ))}
                  </TableCell>
                  <TableCell sx={{ border: "1px solid #ddd" }} align="left">
                    {row.rules.map((ruleObj, index) => (
                      <div key={index}>{ruleObj.query}</div>
                    ))}
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
