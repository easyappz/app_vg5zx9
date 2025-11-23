import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { getToken } from '../../utils/auth';
import { getMessages, sendMessage } from '../../api/messages';
import { getOnlineUsers, sendHeartbeat } from '../../api/users';
import './style.css';

const Chat = () => {
  const navigate = useNavigate();
  const [messages, setMessages] = useState([]);
  const [onlineUsers, setOnlineUsers] = useState([]);
  const [messageText, setMessageText] = useState('');
  const [loading, setLoading] = useState(true);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    const token = getToken();
    if (!token) {
      navigate('/login');
      return;
    }

    loadMessages();
    loadOnlineUsers();

    const messagesInterval = setInterval(() => {
      loadMessages();
    }, 3000);

    const usersInterval = setInterval(() => {
      loadOnlineUsers();
    }, 5000);

    const heartbeatInterval = setInterval(() => {
      sendHeartbeat().catch(err => console.error('Heartbeat error:', err));
    }, 30000);

    sendHeartbeat().catch(err => console.error('Initial heartbeat error:', err));

    return () => {
      clearInterval(messagesInterval);
      clearInterval(usersInterval);
      clearInterval(heartbeatInterval);
    };
  }, [navigate]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadMessages = async () => {
    try {
      const data = await getMessages();
      setMessages(data);
      setLoading(false);
    } catch (error) {
      console.error('Error loading messages:', error);
      if (error.response && error.response.status === 401) {
        navigate('/login');
      }
    }
  };

  const loadOnlineUsers = async () => {
    try {
      const data = await getOnlineUsers();
      setOnlineUsers(data);
    } catch (error) {
      console.error('Error loading online users:', error);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!messageText.trim()) return;

    try {
      await sendMessage(messageText);
      setMessageText('');
      loadMessages();
    } catch (error) {
      console.error('Error sending message:', error);
      if (error.response && error.response.status === 401) {
        navigate('/login');
      }
    }
  };

  const handleProfileClick = () => {
    navigate('/profile');
  };

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="chat-container" data-easytag="id1-react/src/components/Chat/index.jsx">
      <header className="chat-header">
        <h1 className="chat-title">Групповой чат</h1>
        <button className="profile-button" onClick={handleProfileClick}>
          Профиль
        </button>
      </header>

      <div className="chat-content">
        <aside className="online-sidebar">
          <h2 className="sidebar-title">Онлайн ({onlineUsers.length})</h2>
          <ul className="online-users-list">
            {onlineUsers.map((user) => (
              <li key={user.id} className="online-user-item">
                <span className="online-indicator"></span>
                <span className="user-name">{user.full_name || user.username}</span>
              </li>
            ))}
          </ul>
        </aside>

        <main className="messages-area">
          <div className="messages-list">
            {loading ? (
              <div className="loading-message">Загрузка сообщений...</div>
            ) : messages.length === 0 ? (
              <div className="empty-message">Пока нет сообщений. Начните общение!</div>
            ) : (
              messages.map((message) => (
                <div key={message.id} className="message-item">
                  <div className="message-header">
                    <span className="message-author">{message.author_name}</span>
                    <span className="message-time">{formatTime(message.created_at)}</span>
                  </div>
                  <div className="message-text">{message.text}</div>
                </div>
              ))
            )}
            <div ref={messagesEndRef} />
          </div>

          <form className="message-input-form" onSubmit={handleSendMessage}>
            <input
              type="text"
              className="message-input"
              placeholder="Введите сообщение..."
              value={messageText}
              onChange={(e) => setMessageText(e.target.value)}
              maxLength={5000}
            />
            <button type="submit" className="send-button" disabled={!messageText.trim()}>
              Отправить
            </button>
          </form>
        </main>
      </div>
    </div>
  );
};

export default Chat;