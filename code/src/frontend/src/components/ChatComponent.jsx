import { useState } from "react";
import {
  TextField,
  Button,
  Card,
  CardContent,
  InputAdornment,
} from "@mui/material";
import { getChatQueryResponse } from "../service";
import SendIcon from "@mui/icons-material/Send";
import axios from "axios";

export default function ChatComponent() {
  const [messages, setMessages] = useState([
    { text: "Hi! How can I help you?", sender: "bot" },
    {
      text: "Can you tell me which profiling rule is making segment ID 2345 be marked?",
      sender: "user",
    },
    {
      text: "Sure! Its the profiling rule 'UPB<1000' : The segment ID 2345 was marked because the upb is equal to $523, it should ideally be >=$1000.",
      sender: "bot",
    },
    { text: "Oh okay, Got it.", sender: "user" },
    { text: "Do you want to see a remediation rule for it?", sender: "bot" },
    { text: "Yes", sender: "user" },
    {
      text: "First, check if the upb is really $523 since ideally it should be >$1000. If it has a valid reason, We cant really change an UPB, so you can just mark the segment as an exception and also fill hte exception reason accordingly. ",
      sender: "bot",
    },
    { text: "Thanks!", sender: "user" },
    {
      text: "No problem! Do you need help with anything else?",
      sender: "bot",
    },
    { text: "No, Thank You!", sender: "user" },
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

    const newMessages = [...messages, { text: input, sender: "user" }];
    setMessages(newMessages);
    setInput("");

    try {
      const response = getChatQueryResponse(input);
      setMessages([
        ...newMessages,
        { text: response.data.reply, sender: "bot" },
      ]);
    } catch (error) {
      setMessages([
        ...newMessages,
        { text: "Error fetching response", sender: "bot" },
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
