import React, { useState } from 'react';
import ChatWindow from '../components/ChatWindow'; // adjust path if needed

function Chat() {
  // Manage the chat messages as an array in component state
  const [messages, setMessages] = useState([
    { sender: 'Alice', text: 'Hi there!' },
    { sender: 'Bob', text: 'Hello!' },
  ]);

  // Handler for sending a new message
  const handleSendMessage = (messageText) => {
    setMessages([...messages, { sender: 'You', text: messageText }]);
    // Later: connect to backend or WebSocket here to send message to others
  };

  return (
    <div>
      <h2>Chat Interface</h2>
      <ChatWindow messages={messages} onSendMessage={handleSendMessage} />
    </div>
  );
}

export default Chat;
