import React from "react";
import MUIDataTable from "mui-datatables";

function DataTableComponent({ violations }) {
  const columns = [
    {
      name: "row_number",
      label: "Row Number",
      options: {
        setCellHeaderProps: () => ({
          style: { backgroundColor: "#DD1E25", color: "white" },
        }),
      },
    },
    {
      name: "rules_violated",
      label: "Profiling Rules Violated",
      options: {
        customBodyRender: (value) => (
          <div>
            {value.map((item, index) => (
              <div key={index}>→ {item}</div>
            ))}
          </div>
        ), // Render array items as separate lines
        setCellHeaderProps: () => ({
          style: { backgroundColor: "#DD1E25", color: "white" },
        }),
      },
    },
    {
      name: "associated_columns",
      label: "Associated Columns",
      options: {
        customBodyRender: (value) => (
          <div>
            {value.map((item, index) => (
              <div key={index}>→ {item}</div>
            ))}
          </div>
        ), // Render array items as separate lines
        setCellHeaderProps: () => ({
          style: { backgroundColor: "#DD1E25", color: "white" },
        }),
      },
    }
  ];

  const options = {
    filter: true,
    filterType: "dropdown",
    responsive: "standard",
    selectableRows: "none",
    rowsPerPage: 5,
    rowsPerPageOptions: [5, 10, 15],
    download: true,
    search: true,
    viewColumns: true,
    customHeadRender: (columnMeta) => (
      <th
        key={columnMeta.index}
        style={{
          backgroundColor: "#DD1E25",
          color: "white",
          padding: "10px",
          textAlign: "left",
        }}
      >
        {columnMeta.label}
      </th>
    ),
  };

  return (
    <div style={{ margin: "20px", width: "100%" }}>
      <MUIDataTable
        title={
          <h2 style={{ textAlign: "left", marginBottom: "10px", color: "#DD1E25" }}>
            Non-compliant data
          </h2>
        }
        data={violations || []}
        columns={columns}
        options={options}
      />
    </div>
  );
}

export default DataTableComponent;
