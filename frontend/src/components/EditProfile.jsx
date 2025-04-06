import React, { useEffect, useState } from "react";
import { TextField, Button, Avatar, Typography, Box } from "@mui/material";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function EditProfile() {
  const [profile, setProfile] = useState({
    user_name: "",
    user_email: "",
    user_fname: "",
    user_lname: "",
    user_pass: "" 
  });
  const navigate = useNavigate();

  const fetchProfile = async () => {
    try {
      const res = await axios.get("http://localhost:8080/edit-profile", { withCredentials: true });
      setProfile(res.data);
    } catch (error) {
      console.error("Failed to fetch profile", error);
    }
  };

  const handleChange = (e) => {
    setProfile({ ...profile, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://localhost:8080/edit-profile", profile, { withCredentials: true });
      alert("Profile updated!");
      navigate("/");
    } catch (error) {
      console.error("Update failed", error);
    }
  };

  useEffect(() => {
    fetchProfile();
  }, []);



  return (
    <Box sx={{ maxWidth: 400, mx: "auto", mt: 5, p: 3, boxShadow: 3, borderRadius: 2 }}>
      <Box sx={{ display: "flex", justifyContent: "center", mb: 2 }}>
        <Avatar sx={{ width: 56, height: 56 }}>{profile.user_fname?.[0]}</Avatar>
      </Box>
      <Typography variant="h5" align="center" gutterBottom>Edit Profile</Typography>
      <form onSubmit={handleSubmit}>
      <TextField fullWidth label="Username" name="user_name" value={profile.user_name} onChange={handleChange} margin="normal" />
      <TextField fullWidth label="Password" type="password" name="user_pass" value={profile.user_pass || ""} onChange={handleChange} margin="normal" />
        <TextField fullWidth label="First Name" name="user_fname" value={profile.user_fname} onChange={handleChange} margin="normal" />
        <TextField fullWidth label="Last Name" name="user_lname" value={profile.user_lname} onChange={handleChange} margin="normal" />
        <TextField fullWidth label="Email" name="user_email" value={profile.user_email} onChange={handleChange} margin="normal" />
        <Button fullWidth variant="contained" type="submit" sx={{ mt: 2 }}>Save Changes</Button>
      </form>
    </Box>
  );
}
