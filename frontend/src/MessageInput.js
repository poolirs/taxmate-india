import React, { useState } from 'react';

function MessageInput({ onSendMessage }) {
  const [inputValue, setInputValue] = useState('');

  const handleSend = () => {
    if (inputValue.trim()) {
      onSendMessage(inputValue.trim());
      setInputValue('');
    }
  };

  return (
    <div className="message-input">
      <input
        type="text"
        placeholder="Type a message..."
        value={inputValue}
        onChange={e => setInputValue(e.target.value)}
        onKeyDown={e => { if (e.key === 'Enter') handleSend(); }}
      />
      <button onClick={handleSend}>Send</button>
    </div>
  );
}

export default MessageInput;
