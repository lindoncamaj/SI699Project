import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function Register() {
  const navigate = useNavigate();

  const [user_name, setUsername] = useState("");
  const [user_pass, setPassword] = useState("");
  const [user_email, setEmail] = useState("");
  const [user_fname, setFName] = useState("");
  const [user_lname, setLName] = useState("");


  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(user_name, user_pass, user_email, user_fname, user_lname);

    // Validation check: Ensure all fields are filled
    if (!user_name || !user_pass || !user_email || !user_fname || !user_lname) {
      alert("Please fill out all fields before submitting.");
      return;
    }

    const data = {
      user_name,
      user_pass,
      user_email,
      user_fname,
      user_lname
    };

    // Pass form data to flask login function
    axios.post("http://127.0.0.1:8080/register", data).then((response) => {
      alert(response.data.message);
      navigate("/login");
    });
  };
  // Reset all state variables here
  const handleReset = () => {
    setUsername("");
    setPassword("");
    setEmail("");
    setFName("");
    setLName("");
  };
  return (
    <div>
      <h1>Register</h1>
      <fieldset>
        <form action="#" method="get">
          <label htmlFor="user_name">Username</label>
          <input
            type="string"
            name="user_name"
            id="user_name"
            value={user_name}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Enter username"
            required
          />
          <label htmlFor="user_pass">Password</label>
          <input
            type="password"
            name="user_pass"
            id="user_pass"
            value={user_pass}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="*******"
            required
          />
          <label htmlFor="user_email">Email</label>
          <input
            type="string"
            name="user_email"
            id="user_email"
            value={user_email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="123@example.com"
            required
          />
          <label htmlFor="user_fname">First Name</label>
          <input
            type="string"
            name="user_fname"
            id="user_fname"
            value={user_fname}
            onChange={(e) => setFName(e.target.value)}
            placeholder="John"
            required
          />
          <label htmlFor="user_lname">Last Name</label>
          <input
            type="string"
            name="user_lname"
            id="user_lname"
            value={user_lname}
            onChange={(e) => setLName(e.target.value)}
            placeholder="Smith"
            required
          />
          <button
            id="reset"
            type="reset"
            value="reset"
            onClick={() => handleReset()}
          >
            Reset
          </button>
          <button
            id="submit"
            type="submit"
            value="Submit"
            onClick={(e) => handleSubmit(e)}
          >
            Submit
          </button>
        </form>
      </fieldset>
    </div>
  );
}

export default Register;
