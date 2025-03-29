import { useLocation } from "react-router-dom";
import { Card, CardContent, CardActions, CardMedia, Typography, Button, Container, Grid } from "@mui/material";
// import { useState, useEffect } from "react";

const Listings = () => {
    const location = useLocation();
    const listingsData = location.state || {};


    if (!listingsData.length) {
        return <h1 className="text-center text-xl font-bold mt-6">No Listings Found</h1>;
    }


    return (
        <Container>
            <h1 className="text-2xl font-bold text-center mb-6">Listings</h1>
            <Grid container spacing={3}>
                {listingsData.map((listing, index) => (
                    <Grid item xs={12} sm={6} md={4} key={index}>
                        <Card className="shadow-md">
                            <CardMedia
                                component="img"
                                height="140"
                                image={listing.media.photo_links[0] || "https://static.vecteezy.com/system/resources/thumbnails/002/083/833/small/red-car-illustration-free-vector.jpg"} // Placeholder if no image
                                alt={listing.heading}
                            />
                            <CardContent>
                                <Typography variant="h6" component="div">
                                    {listing.heading}
                                </Typography>
                            </CardContent>
                            <CardActions>
                                <Button
                                    variant="contained"
                                    color="primary"
                                    href={listing.vdp_url}
                                    target="_blank"
                                    rel="noopener noreferrer"
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


export default Listings;