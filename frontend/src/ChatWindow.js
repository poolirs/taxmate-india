import React from 'react';
import Message from './Message';
import MessageInput from './MessageInput';

function ChatWindow({ messages, onSendMessage }) {
  return (
    <div className="chat-window">
      <div className="messages-list" style={{ height: '300px', overflowY: 'scroll', border: '1px solid #ccc', padding: '10px' }}>
        {messages.map((msg, index) => (
          <Message key={index} sender={msg.sender} text={msg.text} />
        ))}
      </div>
      <MessageInput onSendMessage={onSendMessage} />
    </div>
  );
}

export default ChatWindow;
