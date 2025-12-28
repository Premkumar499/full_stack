import { useState } from "react";
import { login, getProfile } from "../api/api";
import "../styles/auth.css";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    const res = await login({ email, password });

    if (res.token) {
      localStorage.setItem("token", res.token);

      const user = await getProfile(res.token);
      localStorage.setItem("user", JSON.stringify(user));

      window.location.href = "/profile";
    } else {
      alert(res.error);
    }
  };

  return (
    <div className="auth-box">
      <h2>Login</h2>
      <input placeholder="Email" onChange={e => setEmail(e.target.value)} />
      <input type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} />
      <button onClick={handleLogin}>Login</button>
    </div>
  );
}

export default Login;
