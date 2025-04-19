import React, { useEffect, useState } from "react";
import { Avatar, Box, Typography, CircularProgress } from "@mui/material";
import axios from "axios";

export default function Profile() {
    const [profile, setProfile] = useState({
        user_name: "",
        user_email: "",
        user_fname: "",
        user_lname: "",
      });

    const fetchProfile = async () => {
        try {
          const res = await axios.get("http://127.0.0.1:8080/profile", { withCredentials: true });
          setProfile(res.data);
        } catch (error) {
          console.error("Failed to fetch profile", error);
        }
    };

    useEffect(() => {
        fetchProfile();
    }, []);

    return (
      <div>
        <Box sx={{ display: "flex", justifyContent: "center", mb: 2 }}>
            <Avatar sx={{ width: 56, height: 56 }}>{profile.user_fname?.[0]}</Avatar>
        </Box>
        <Typography variant="h6" sx={{ marginLeft: 1 }}>
            {profile.user_name}
        </Typography>
        <Typography variant="body1">
            Name: {profile.user_fname} {profile.user_lname}
        </Typography>
        <Typography variant="body1">
            Email: {profile.user_email}
        </Typography>
      </div>
    );
  };