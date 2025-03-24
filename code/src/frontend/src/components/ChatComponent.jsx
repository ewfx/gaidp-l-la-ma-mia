import { useState } from "react";
import {
  TextField,
  Button,
  Card,
  CardContent,
  InputAdornment,
} from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import axios from "axios";

export default function ChatComponent() {
  const [messages, setMessages] = useState([
    { text: "Hi! How can I help you?", sender: "bot" },
  ]);
  const [input, setInput] = useState("");

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
      // Make a POST request to the chat endpoint
      const response = await axios.post("http://127.0.0.1:8000/chat/", {
        message: input,
      });
  
      // Log the response to inspect its structure
      console.log("Response data:", response.data.data);
  
      // Extract the message or convert the object to a string
      const botReply =
        typeof response.data.data === "string"
          ? response.data.data
          : JSON.stringify(response.data.data);
  
      // Add the system's reply to the chat
      setMessages([...newMessages, { text: botReply, sender: "bot" }]);
    } catch (error) {
      console.error("Error fetching response:", error);
      setMessages([
        ...newMessages,
        { text: "Error fetching response from the server.", sender: "bot" },
      ]);
    }
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
                padding: "8px 12px",
                borderRadius: "8px",
                maxWidth: "60%",
                alignSelf: msg.sender === "user" ? "flex-end" : "flex-start",
                backgroundColor: msg.sender === "user" ? "#1D62FC" : "#343146",
                color: "white",
              }}
            >
              {msg.text}
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
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type a message..."
        />
      </div>
    </div>
  );
}
