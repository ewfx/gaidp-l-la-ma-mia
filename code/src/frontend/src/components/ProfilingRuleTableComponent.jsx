import React from "react";
import MUIDataTable from "mui-datatables";

function ProfilingRuleTableComponent({ profilingRuleData }) {
  const columns = [
    {
      name: "fieldName",
      label: "Associated Column",
      options: {
        setCellHeaderProps: () => ({
          style: { backgroundColor: "#DD1E25", color: "white" },
        }),
      },
    },
    {
      name: "rule",
      label: "Profiling Rule",
      options: {
        setCellHeaderProps: () => ({
          style: { backgroundColor: "#DD1E25", color: "white" },
        }),
      },
    },
    {
      name: "query",
      label: "Query",
      options: {
        setCellHeaderProps: () => ({
          style: { backgroundColor: "#DD1E25", color: "white" },
        }),
      },
    },
    {
      name: "pageNumber",
      label: "Page Number",
      options: {
        setCellHeaderProps: () => ({
          style: { backgroundColor: "#DD1E25", color: "white" },
        }),
      },
    },
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
    <div style={{ margin: "20px" }}>
      <MUIDataTable
        title={<h2 style={{ textAlign: "left", marginBottom: "10px", color: "#DD1E25" }}>
          Profiling Rules
        </h2>
        }
        data={profilingRuleData || []}
        columns={columns}
        options={options}
      />
    </div>
  );
}

export default ProfilingRuleTableComponent;
