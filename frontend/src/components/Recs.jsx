import { useLocation, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from "axios";
import { Card, CardContent, CardActions, CardMedia, Typography, Button, Container, Grid } from "@mui/material";
// import Grid from '@mui/material/Grid2';

const Recs = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const formData = location.state || {}; // Get form data from state

  const handleLinkClick = (query_id, selection_rank, make, model, year, zip) => {
    const data = {
      "query_id": query_id,
      "selection_rank": selection_rank,
      "make": make,
      "model": model,
      "year": year,
      "zip": zip
    }
    // Navigate to the recommendations page with the car make as a query parameter
    axios.post("http://0.0.0.0:8080/lists", data, { withCredentials: true }).then((response) => {navigate("/listings", {state: response.data})});
  };


  return (
    <Container>
      <Typography variant="h4" align="center" gutterBottom>
        Recommendations
      </Typography>
      <Grid container spacing={3}>
        {Object.keys(formData).map((key) => (
          <Grid item xs={12} sm={6} md={4} key={key}>
            <Card>
              <CardMedia
                component="img"
                height="140"
                image={formData[key].image}// Placeholder image
                alt={`${formData[key].make} ${formData[key].model}`}
              />
              <CardContent>
                <Typography variant="h6">
                  {formData[key].year} {formData[key].make} {formData[key].model}
                </Typography>
              </CardContent>
              <CardActions>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={() => handleLinkClick(formData[key].query_id, key, formData[key].make, formData[key].model, formData[key].year, formData[key].zip)}
                >
                  View Details
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
};

export default Recs;
