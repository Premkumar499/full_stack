import { Link } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
  const user = JSON.parse(localStorage.getItem("user"));

  const logout = () => {
    localStorage.clear();
    window.location.href = "/login";
  };

  return (
    <div className="navbar">
      <Link to="/profile" className="nav-link">Profile</Link>

      {user?.role === "admin" && (
        <Link to="/add-topic" className="nav-link">
          Add Topic
        </Link>
      )}

      <span className="user-email">{user?.email}</span>
      <button onClick={logout} className="logout-btn">Logout</button>
    </div>
  );
}

export default Navbar;
