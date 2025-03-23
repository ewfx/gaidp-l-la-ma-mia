import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Menu,
  MenuItem,
  Box,
  IconButton,
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import HomeComponent from "./pages/HomeComponent/HomeComponent";
import "./App.css";
import ProfilingRulesComponent from "./pages/ProfilingRulesComponent/ProfilingRulesComponent";
import DataComponent from "./pages/DataComponent/DataComponent";

function App() {
  const [anchorEl, setAnchorEl] = useState(null);

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <Router>
      <div className="App">
        <AppBar position="static" style={{ backgroundColor: "#DD1E25" }}>
          <Toolbar sx={{ height: "64px" }}>
            <Typography
              variant="h6"
              component="div"
              sx={{
                position: "absolute",
                left: "50%",
                transform: "translateX(-50%)",
                fontWeight: "bold",
              }}
            >
              Data Profiler
            </Typography>
            <Box sx={{ flexGrow: 1 }} />
            <div style={{ marginLeft: "auto" }}>
              <Button color="inherit" component={Link} to="/">
                Home
              </Button>
              <Button color="inherit" component={Link} to="/profiling">
                Profiling
              </Button>
            </div>
            <Menu
              id="menu-appbar"
              anchorEl={anchorEl}
              anchorOrigin={{
                vertical: "top",
                horizontal: "right",
              }}
              keepMounted
              transformOrigin={{
                vertical: "top",
                horizontal: "right",
              }}
              open={Boolean(anchorEl)}
              onClose={handleClose}
            >
              <MenuItem onClick={handleClose} component={Link} to="/">
                Home
              </MenuItem>
              <MenuItem onClick={handleClose} component={Link} to="/profiling">
                Profiling
              </MenuItem>
            </Menu>
          </Toolbar>
        </AppBar>
        <Routes>
          <Route path="/" element={<HomeComponent />} />
          <Route path="/profiling" element={<ProfilingRulesComponent />} />
          {/* Add other routes here */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
