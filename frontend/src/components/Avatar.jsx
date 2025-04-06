// components/ProfileAvatar.jsx
import { useNavigate } from "react-router-dom";
import { Avatar, IconButton, Tooltip } from "@mui/material";

function ProfileAvatar() {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate("/edit-profile");
  };

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
          <Avatar alt="User" src=""/>
        </IconButton>
      </Tooltip>
         </div>
  );
}

export default ProfileAvatar;
