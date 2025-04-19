import { useNavigate } from "react-router-dom";
import { Avatar, IconButton, Tooltip, Menu, MenuItem } from "@mui/material";
import { useEffect, useState } from "react";
import { useAuth } from '../context/AuthContext';
import axios from "axios";


function ProfileAvatar() {
  const navigate = useNavigate();
  const { isLoggedIn, login, logout } = useAuth();
  const [loading, setLoading] = useState(true);
  const [anchorEl, setAnchorEl] = useState(null);

  useEffect(() => {
    const checkLoginStatus = async () => {
      try {
        const res = await axios.get("http://127.0.0.1:8080/session", {
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


  const handleClick = (event) => {
    setAnchorEl(event.currentTarget); // open the dropdown
  };

  const handleClose = () => {
    setAnchorEl(null); // close the dropdown
  };

  const handleMenuItemClick = (option) => {
    handleClose(); // close the dropdown
    if (option === "profile") {
      navigate("/profile");
    } else if (option === "settings") {
      navigate("/edit-profile");
    } else if (option === "logout") {
      handleLogout(); // Call the handleLogout function
    } else if (option === "login") {
      navigate("/login");
    }
  };

  const handleLogout = async () => {
    try {
      await axios.post(
        "http://127.0.0.1:8080/logout",
        {},
        { withCredentials: true }
      ).then((response) => { navigate("/", { state: response.data });});
      logout(); // Call logout from context
    } catch (error) {
      console.error("Logout error:", error);
    }
  };



  // 🔒 Don't render anything until session check is done
  // if (loading || !isLoggedIn) return null;
  if (loading) return null;

  return (
    <div
      style={{
        position: "absolute",
        top: "1rem",
        right: "1rem",
        zIndex: 1000,
      }}
    >
      <Tooltip title="Profile Options">
        <IconButton onClick={handleClick}>
          <Avatar alt="User" src="" />
        </IconButton>
      </Tooltip>

      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleClose}
      >
        {isLoggedIn ? (
          <>
            <MenuItem onClick={() => handleMenuItemClick("profile")}>Profile</MenuItem>
            <MenuItem onClick={() => handleMenuItemClick("settings")}>Settings</MenuItem>
            <MenuItem onClick={() => handleMenuItemClick("logout")}>Logout</MenuItem>
          </>
        ) : (
          <MenuItem onClick={() => handleMenuItemClick("login")}>Login</MenuItem>
        )}
      </Menu>
    </div>
  );
}

export default ProfileAvatar;
