import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from '../context/AuthContext';
import axios from "axios";

function Login() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [user_name, setUsername] = useState("");
  const [user_pass, setPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(user_name, user_pass);

    // Validation check: Ensure all fields are filled
    if (!user_name || !user_pass) {
      alert("Please fill out all fields before submitting.");
      return;
    }

    const data = {
      user_name,
      user_pass
    };

    // Pass form data to flask login function
    axios.post("http://127.0.0.1:8080/login", data, { withCredentials: true }).then((response) => {
      alert(response.data.message);
      if (response.data.message === "Successfully Logged-in") {
        login();
        navigate("/");
      } else {
        navigate("/login");
      }
    });
  };
  // Reset all state variables here
  const handleReset = () => {
    setUsername("");
    setPassword("");
  };

  const handleRegisterClick = () => {
    navigate("/register");
  };
  return (
    <div>
      <h1>Login</h1>
      <a href="#" onClick={handleRegisterClick}>Register</a>
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

export default Login;
