import Navbar from "../components/Navbar";
import "../styles/profile.css";

function Profile() {
  const user = JSON.parse(localStorage.getItem("user"));

  return (
    <>
      <Navbar />
      <div className="profile-box">
        <h2>Profile</h2>
        <p>Email: {user?.email}</p>
        <p>Role: {user?.role}</p>
      </div>
    </>
  );
}

export default Profile;
