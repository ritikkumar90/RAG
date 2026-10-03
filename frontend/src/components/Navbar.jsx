import React from 'react';
import './Navbar.css';

const Navbar = ({ isAuthenticated, userName, onLogout, onLoginClick }) => {
  return (
    <nav className="navbar">
      <div className="nav-brand">
        RAG Assistant
      </div>
      
      <div className="nav-links">
        <a href="#home" className="nav-link">Home</a>
        <a href="#chat" className="nav-link">Chat</a>
        <a href="#documents" className="nav-link">Documents</a>
      </div>

      <div className="nav-actions">
        {isAuthenticated ? (
          <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
            <span style={{ color: '#fff', fontWeight: 'bold' }}>Hello, {userName}</span>
            <button className="nav-btn nav-btn-outline" onClick={onLogout}>Logout</button>
          </div>
        ) : (
          <>
            <button className="nav-btn nav-btn-outline" onClick={onLoginClick}>Log In</button>
            <button className="nav-btn nav-btn-primary" onClick={onLoginClick}>Sign Up</button>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
