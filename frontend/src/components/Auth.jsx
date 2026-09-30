import { useState } from "react";
import "./Auth.css";

export default function Auth({ onLogin }) {
  const [isLogin, setIsLogin] = useState(true);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (onLogin) onLogin();
  };

  return (
    <div className="auth-container">
      <div className={`auth-card ${isLogin ? "login" : "signup"}`}>
        <div className="auth-header">
          <h2>{isLogin ? "Welcome Back" : "Create Account"}</h2>
          <p>
            {isLogin
              ? "Enter your details to access your account"
              : "Sign up to get started with our platform"}
          </p>
        </div>

        <form className="auth-form" onSubmit={handleSubmit}>
          {!isLogin && (
            <div className="form-group">
              <label htmlFor="name">Full Name</label>
              <input type="text" id="name" placeholder="John Doe" required />
            </div>
          )}
          <div className="form-group">
            <label htmlFor="email">Email Address</label>
            <input
              type="email"
              id="email"
              placeholder="john@example.com"
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              placeholder="••••••••"
              required
            />
          </div>

          {isLogin && (
            <a href="#" className="forgot-password">
              Forgot password?
            </a>
          )}

          <button type="submit" className="auth-submit">
            {isLogin ? "Sign In" : "Sign Up"}
          </button>
        </form>

        <div className="auth-footer">
          <p>
            {isLogin ? "Don't have an account? " : "Already have an account? "}
            <button
              type="button"
              className="toggle-btn"
              onClick={() => setIsLogin(!isLogin)}
            >
              {isLogin ? "Sign up" : "Log in"}
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}
