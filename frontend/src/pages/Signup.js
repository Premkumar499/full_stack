import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { signup } from "../api/api";
import "../styles/auth.css";

function Signup() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSignup = async () => {
    const res = await signup({ email, password });
    if (!res.error) {
      alert(res.message || "OTP sent to email");
      // Navigate to verify page with email
      navigate("/verify", { state: { email } });
    } else {
      alert(res.error);
    }
  };

  return (
    <div className="auth-box">
      <h2>Signup</h2>
      <input placeholder="Email" onChange={e => setEmail(e.target.value)} />
      <input type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} />
      <button onClick={handleSignup}>Signup</button>
      <p>Already have an account? <a href="/login">Login</a></p>
    </div>
  );
}

export default Signup;
