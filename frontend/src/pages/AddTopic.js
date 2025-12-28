import { useState } from "react";
import { addTopic } from "../api/api";
import Navbar from "../components/Navbar";
import "../styles/admin.css";

function AddTopic() {
  const [title, setTitle] = useState("");
  const token = localStorage.getItem("token");

  const handleAdd = async () => {
    const res = await addTopic(token, { title });
    alert(res.message || res.error);
  };

  return (
    <>
      <Navbar />
      <div className="admin-box">
        <h2>Add Topic (Admin)</h2>
        <input placeholder="Topic title" onChange={e => setTitle(e.target.value)} />
        <button onClick={handleAdd}>Add Topic</button>
      </div>
    </>
  );
}

export default AddTopic;
