import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

function HomeComponent() {
  const navigate = useNavigate();
  const [position, setPosition] = useState(-100);

  useEffect(() => {
    const interval = setInterval(() => {
      setPosition((prev) => (prev > window.innerWidth ? -100 : prev + 5));
    }, 80);
    return () => clearInterval(interval);
  }, []);

  return (
    <div
      style={{
        textAlign: "center",
        height: "calc(100vh - 64px)",
        position: "relative",
        overflow: "hidden",
      }}
    >
      <h1
        style={{ fontSize: "2.5rem", marginBottom: "20px", marginTop: "50px" }}
      >
        Simplifying Data Profiling & Anomaly Detection
      </h1>
      <p style={{ fontSize: "1.2rem", marginBottom: "40px" }}>
        Empowering the Organization with smarter insights and cleaner data.
      </p>
      <button
        onClick={() => navigate("/profiling")}
        style={{
          padding: "15px 30px",
          fontSize: "1rem",
          backgroundColor: "#007BFF",
          color: "#fff",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer",
        }}
      >
        Get Started
      </button>
      <img
        src="https://media.tenor.com/lRRpO4qTF3AAAAAj/llama-walking-llama.gif"
        alt="Walking Animal"
        style={{
          position: "absolute",
          bottom: "0px", // Ensures the image aligns with the bottom border
          left: `${position}px`,
          height: "300px", // Adjusted height for better fit along the bottom
          transform: "scaleX(-1)", // Flips the image horizontally
        }}
      />
    </div>
  );
}

export default HomeComponent;
