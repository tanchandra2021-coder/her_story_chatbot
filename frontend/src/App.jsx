import React, { useState } from "react";
import axios from "axios";
import "./App.css";

const LEADERS = ["Michelle Obama", "Frida Kahlo", "Marie Curie", "Rosa Parks", "Malala Yousafzai"];

function App() {
  const [leader, setLeader] = useState(LEADERS[0]);
  const [input, setInput] = useState("");
  const [history, setHistory] = useState([]);

  const sendMessage = async () => {
    if (!input) return;
    const userMsg = { sender: "You", text: input };
    try {
      const res = await axios.post("http://localhost:8000/chat", {
        leader,
        user_input: input
      });
      setHistory(prev => [...prev, userMsg, { sender: leader, text: res.data.response }]);
    } catch (err) {
      setHistory(prev => [...prev, userMsg, { sender: leader, text: "Error contacting server" }]);
    }
    setInput("");
  };

  return (
    <div className="App">
      <h1>Her Story Chatbot</h1>
      <select value={leader} onChange={(e) => setLeader(e.target.value)}>
        {LEADERS.map(l => <option key={l}>{l}</option>)}
      </select>
      <div className="chat-box">
        {history.map((msg, idx) => (
          <p key={idx}><strong>{msg.sender}:</strong> {msg.text}</p>
        ))}
      </div>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type your question..."
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}

export default App;

