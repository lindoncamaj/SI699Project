import { useNavigate } from "react-router-dom";
import { Avatar, IconButton, Tooltip } from "@mui/material";
import axios from "axios";
import { useEffect, useState } from "react";
import { useAuth } from '../context/AuthContext';


function ProfileAvatar() {
  const navigate = useNavigate();
  const { isLoggedIn, login, logout } = useAuth();
  const [loading, setLoading] = useState(true); // to avoid flicker

  useEffect(() => {
    const checkLoginStatus = async () => {
      try {
        const res = await axios.get("http://localhost:8080/session", {
          withCredentials: true,
        });
        if (res.data.logged_in) {
          login();
        } else {
          logout();
        }
      } catch (error) {
        console.error("Session check failed:", error);
        logout();
      } finally {
        setLoading(false);
      }
    };

    checkLoginStatus();
  }, [login, logout]);

  const handleClick = () => {
    navigate("/edit-profile");
  };

  // 🔒 Don't render anything until session check is done
  if (loading || !isLoggedIn) return null;

  return (
    <div
      style={{
        position: "fixed",
        top: "1rem",
        right: "1rem",
        zIndex: 1000,
      }}
    >
      <Tooltip title="Edit Profile">
        <IconButton onClick={handleClick}>
          <Avatar alt="User" src="" />
        </IconButton>
      </Tooltip>
    </div>
  );
}

export default ProfileAvatar;
