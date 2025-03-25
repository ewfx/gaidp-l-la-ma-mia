import { useState } from "react";
import {
  TextField,
  Button,
  Card,
  CardContent,
  InputAdornment,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Menu,
  MenuItem,
} from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import axios from "axios";

export default function ChatComponent({ pdfName, schedule, category, fetchProfilingRules, dataCollectionName, fetchViolations, profilingRuleData }) {
  const initialBotMessage = {
    text: "Hi! You can modify rule in simple language by identifying field using a #. For example, #age should not be negative",
    sender: "bot",
  };

  const [messages, setMessages] = useState([initialBotMessage]);
  const [input, setInput] = useState("");
  const [confirmDialogOpen, setConfirmDialogOpen] = useState(false);
  const [pendingUpdate, setPendingUpdate] = useState(null); // Store the pending update
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [anchorEl, setAnchorEl] = useState(null);

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      sendMessage();
    }
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    // Add the user's message to the chat
    const newMessages = [...messages, { text: input, sender: "user" }];
    setMessages(newMessages);
    setInput("");

    try {
      if (!(pdfName && schedule && category)) {
        setMessages([
          ...newMessages,
          { text: "Please select a pdf, schedule and category first.", sender: "bot" },
        ]);
        return;
      }

      // Encode the input to ensure special characters are handled properly
      const encodedInput = encodeURIComponent(input);

      // Make a POST request to the chat endpoint
      const response = await axios.post(
        `http://127.0.0.1:8000/chat?message=${encodedInput}&pdfName=${pdfName}&schedule=${schedule}&category=${category}`
      );

      // Extract the response from the backend
      const botReply =
        typeof response.data.data === "string"
          ? response.data.data
          : JSON.stringify(response.data.data.rule);

      // Add the system's reply to the chat
      setMessages([...newMessages, { text: botReply, sender: "bot" }]);

      // Store the pending update and open the confirmation dialog
      setPendingUpdate(response.data.data);
      setConfirmDialogOpen(true);
    } catch (error) {
      console.error("Error fetching response:", error);
      setMessages([
        ...newMessages,
        { text: "Error fetching response from the server.", sender: "bot" },
      ]);
    }
  };

  const confirmUpdate = async () => {
    if (!pendingUpdate) return;

    try {
      // Make a POST request to update the rule in the database
      const response = await axios.post(`http://127.0.0.1:8000/chat/update?pdfName=${pdfName}&schedule=${schedule}&category=${category}`, {
        updated_rule: pendingUpdate,
      });

      if (response.data.isSuccess) {
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: "Changes have been successfully updated in the database.", sender: "bot" },
          initialBotMessage, // Add the starting prompt after the success message
        ]);
        fetchProfilingRules(pdfName, schedule, category); // Fetch the updated rules
        dataCollectionName && fetchViolations(pdfName, schedule, category, dataCollectionName); // Fetch the updated
      } else {
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: "Failed to update changes in the database.", sender: "bot" },
        ]);
      }
    } catch (error) {
      console.error("Error updating the database:", error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: "Error updating the database.", sender: "bot" },
      ]);
    } finally {
      setConfirmDialogOpen(false);
      setPendingUpdate(null);
    }
  };

  const cancelUpdate = () => {
    setConfirmDialogOpen(false);
    setPendingUpdate(null);
    setMessages([
      initialBotMessage,
      { text: "Changes were not confirmed and have been discarded.", sender: "bot" },
    ]);
  };

  const handleInputChange = (e) => {
    const value = e.target.value;
    setInput(value);

    // Show dropdown if the user types "#"
    if (value.endsWith("#")) {
      setDropdownOpen(true);
      setAnchorEl(e.currentTarget);
    } else {
      setDropdownOpen(false);
    }
  };

  const handleDropdownSelect = (column) => {
    setInput((prev) => `${prev}${column} `);
    setDropdownOpen(false);
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100%",
        backgroundColor: "#24222F",
        color: "white",
      }}
    >
      <Card
        style={{
          flex: 1,
          overflowY: "scroll",
          backgroundColor: "#24222F",
          padding: "16px",
        }}
      >
        <CardContent
          style={{ display: "flex", flexDirection: "column", gap: "8px" }}
        >
          {messages.map((msg, index) => (
            <div
              key={index}
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: msg.sender === "user" ? "flex-end" : "flex-start",
                gap: "8px",
                marginBottom: "8px",
              }}
            >
              {msg.sender === "bot" && (
                <img
                  src="/llamamia_logo.png" // Path to the bot's profile icon
                  alt="Bot"
                  style={{
                    width: "32px",
                    height: "32px",
                    borderRadius: "50%",
                  }}
                />
              )}
              <div
                style={{
                  padding: "8px 12px",
                  borderRadius: "8px",
                  maxWidth: "60%",
                  backgroundColor: msg.sender === "user" ? "#1D62FC" : "#343146",
                  color: "white",
                }}
              >
                {msg.text}
              </div>
            </div>
          ))}
        </CardContent>
      </Card>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "8px",
          marginTop: "16px",
          backgroundColor: "#24222F",
          padding: "8px",
          borderRadius: "8px",
        }}
      >
        <TextField
          fullWidth
          variant="outlined"
          InputProps={{
            style: {
              color: "white",
              backgroundColor: "#1E1C27",
              borderRadius: "8px",
            },
            endAdornment: (
              <InputAdornment position="end">
                <Button
                  onClick={sendMessage}
                  variant="contained"
                  color="primary"
                  sx={{
                    backgroundColor: "#1D62FC",
                    borderRadius: "50%",
                    minWidth: "40px",
                    width: "40px",
                    height: "40px",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    padding: "8px",
                  }}
                >
                  <SendIcon sx={{ color: "white", marginLeft: "3px" }} />
                </Button>
              </InputAdornment>
            ),
          }}
          value={input}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          placeholder="Type a message..."
        />
        <Menu
          anchorEl={anchorEl}
          open={dropdownOpen}
          onClose={() => setDropdownOpen(false)}
        >
          {profilingRuleData &&
            profilingRuleData.map((rule, index) => (
              <MenuItem key={index} onClick={() => handleDropdownSelect(rule.fieldName)}>
                {rule.fieldName}
              </MenuItem>
            ))}
        </Menu>
      </div>

      {/* Confirmation Dialog */}
      <Dialog
        open={confirmDialogOpen}
        onClose={cancelUpdate}
        aria-labelledby="confirm-dialog-title"
        aria-describedby="confirm-dialog-description"
      >
        <DialogTitle id="confirm-dialog-title">Confirm Changes</DialogTitle>
        <DialogContent>
          <DialogContentText id="confirm-dialog-description">
            Do you want to confirm the following changes and update the database?
          </DialogContentText>
          <pre style={{ backgroundColor: "#f4f4f4", padding: "8px", borderRadius: "4px" }}>
            {JSON.stringify(pendingUpdate, null, 2)}
          </pre>
        </DialogContent>
        <DialogActions>
          <Button onClick={cancelUpdate} color="secondary">
            Cancel
          </Button>
          <Button onClick={confirmUpdate} color="primary" autoFocus>
            Confirm
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
