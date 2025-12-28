import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { verifyOtp } from "../api/api";
import "../styles/auth.css";

function VerifyOtp() {
  const [email, setEmail] = useState("");
  const [otp, setOtp] = useState("");
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    // Get email from navigation state if available
    if (location.state?.email) {
      setEmail(location.state.email);
    }
  }, [location.state]);

  const handleVerify = async () => {
    const res = await verifyOtp({ email, otp });
    if (!res.error) {
      alert(res.message || "OTP verified successfully!");
      navigate("/login");
    } else {
      alert(res.error || "Verification failed");
    }
  };

  return (
    <div className="auth-box">
      <h2>Verify OTP</h2>
      <input 
        placeholder="Email" 
        value={email}
        onChange={e => setEmail(e.target.value)} 
      />
      <input placeholder="OTP" onChange={e => setOtp(e.target.value)} />
      <button onClick={handleVerify}>Verify</button>
    </div>
  );
}

export default VerifyOtp;
