import React from "react";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

function DataTableComponent({
  profiledData
}) {
  return(
      <TableContainer component={Paper} sx={{ border: '1px solid #ccc' }}>
      <Table sx={{ minWidth: 650}} aria-label="simple table">
        <TableHead sx={{ backgroundColor: 'beige' }}>
          <TableRow>
            <TableCell sx={{ border: '1px solid #ddd' }} align="left">Data ID</TableCell>
            <TableCell sx={{ border: '1px solid #ddd' }} align="left">Profiling Rule Violated</TableCell>
            <TableCell sx={{ border: '1px solid #ddd' }} align="left">Associated Column</TableCell>
            <TableCell sx={{ border: '1px solid #ddd' }} align="left">Remediation</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {profiledData.map((row) => (
            <TableRow
              key={row.id}
            >
              <TableCell  sx={{ border: '1px solid #ddd' }} align="left">{row.id}</TableCell>
              <TableCell  sx={{ border: '1px solid #ddd' }} align="left">{row.profilingRuleViolated}</TableCell>
              <TableCell  sx={{ border: '1px solid #ddd' }} align="left">{row.column}</TableCell>
              <TableCell  sx={{ border: '1px solid #ddd' }} align="left">{row.remediation}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}

export default DataTableComponent;
