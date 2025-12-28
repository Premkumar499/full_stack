import { BrowserRouter, Routes, Route } from "react-router-dom";
import Signup from "./pages/Signup";
import VerifyOtp from "./pages/VerifyOtp";
import Login from "./pages/Login";
import Profile from "./pages/Profile";
import AddTopic from "./pages/AddTopic";

import PrivateRoute from "./components/PrivateRoute";
import AdminRoute from "./components/AdminRoute";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Signup />} />
        <Route path="/verify" element={<VerifyOtp />} />
        <Route path="/login" element={<Login />} />

        <Route
          path="/profile"
          element={
            <PrivateRoute>
              <Profile />
            </PrivateRoute>
          }
        />

        <Route
          path="/add-topic"
          element={
            <PrivateRoute>
              <AdminRoute>
                <AddTopic />
              </AdminRoute>
            </PrivateRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
