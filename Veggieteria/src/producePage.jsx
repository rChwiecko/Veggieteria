import React from 'react';
import { Card, CardMedia, CardContent, Button, Typography, Grid, Box } from '@mui/material';
import './App.css';

function ImageCard({ image, index }) {
  const handleClick = () => {
    window.open(image.url, '_blank');
  };

  return (
    <Card className="custom-card">
      <CardMedia
        component="img"
        className="custom-image"
        image={image.src}
        alt={image.label}
      />
      <CardContent>
        <Typography gutterBottom variant="h5" component="div">
          {image.label}
        </Typography>
        <Button className="custom-button" variant="contained" onClick={handleClick}>
          View
        </Button>
      </CardContent>
    </Card>
  );
}

// Import images manually
import img1 from './Grocers/image1.png';
import img2 from './Grocers/image2.png';
import img3 from './Grocers/image3.png';
import img4 from './Grocers/image4.png';

const images = [
  { src: img1, label: 'Image 1', url: 'https://www.walmart.com/' },
  { src: img2, label: 'Image 2', url: 'https://www.costco.com/' },
  { src: img3, label: 'Image 3', url: 'https://www.kroger.com/' },
  { src: img4, label: 'Image 4', url: 'https://www.target.com/' },
];

function ProduceShop() {
  return (
    <Box className="main-content">
      <Typography variant="h4" gutterBottom>
        Image Store
      </Typography>
      <Grid container spacing={2}>
        {images.map((image, index) => (
          <Grid item key={index} xs={12} sm={6} md={4} lg={3}>
            <ImageCard image={image} index={index} />
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}

export default ProduceShop;
