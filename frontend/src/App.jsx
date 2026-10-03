import { useState, useEffect } from "react";
import heroImg from "./assets/hero.png";
import reactLogo from "./assets/react.svg";
import viteLogo from "./assets/vite.svg";
import "./App.css";
import Auth from "./components/Auth";
import Chat from "./components/Chat";
import Navbar from "./components/Navbar";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isGuest, setIsGuest] = useState(false);
  const [userName, setUserName] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      setIsAuthenticated(true);
      fetchUserProfile(token);
    }
  }, []);

  const fetchUserProfile = async (token) => {
    try {
      const response = await fetch("http://127.0.0.1:8000/auth/profile", {
        headers: {
          "Authorization": `Bearer ${token}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setUserName(data.user_name);
      }
    } catch (err) {
      console.error("Failed to fetch user profile", err);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setIsAuthenticated(false);
    setIsGuest(false);
    setUserName("");
  };

  return (
    <>
      <Navbar 
        isAuthenticated={isAuthenticated}
        userName={userName}
        onLogout={handleLogout}
        onLoginClick={() => { setIsGuest(false); setIsAuthenticated(false); }}
      />
      {(!isAuthenticated && !isGuest) ? (
        <Auth 
          onLogin={(token) => { setIsAuthenticated(true); fetchUserProfile(token); }} 
          onGuest={() => setIsGuest(true)}
        />
      ) : (
        <Chat />
      )}
    </>
  );
}

export default App;
