const API_URL = "http://127.0.0.1:5000";

export const signup = async (data) => {
  const res = await fetch(`${API_URL}/auth/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
};

export const sendOtp = async (data) => {
  const res = await fetch(`${API_URL}/auth/send-otp`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
};

export const verifyOtp = async (data) => {
  const res = await fetch(`${API_URL}/auth/verify-otp`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
};

export const login = async (data) => {
  const res = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
};

export const getProfile = async (token) => {
  const res = await fetch(`${API_URL}/profile`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.json();
};

export const addTopic = async (token, data) => {
  const res = await fetch(`${API_URL}/topic`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(data),
  });
  return res.json();
};
