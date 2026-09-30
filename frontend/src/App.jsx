import { useState } from "react";
import heroImg from "./assets/hero.png";
import reactLogo from "./assets/react.svg";
import viteLogo from "./assets/vite.svg";
import "./App.css";
import Auth from "./components/Auth";
import Chat from "./components/Chat";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  return (
    <>
      <Chat />
    </>
  );
}

export default App;
