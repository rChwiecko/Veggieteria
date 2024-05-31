import React from 'react';
import { Card, CardMedia, CardContent, Button, Typography, Grid, Box } from '@mui/material';
import './App.css';

function ImageCard({ image }) {
  return (
    <Card className="custom-card">
      <CardMedia
        component="img"
        height="140"
        image={image.src}
        alt={image.label}
      />
      <CardContent>
        <Typography gutterBottom variant="h5" component="div">
          {image.label}
        </Typography>
        <Button className="custom-button" variant="contained">
          View
        </Button>
      </CardContent>
    </Card>
  );
}

// Import images manually
import img1 from './assets/image1.png';
import img2 from './assets/image2.png';
import img3 from './assets/image3.png';
import img4 from './assets/image4.png';
import img5 from './assets/image5.png';
import img6 from './assets/image6.png';
import img7 from './assets/image7.png';
import img8 from './assets/image8.png';

const images = [
  { src: img1, label: 'Image 1' },
  { src: img2, label: 'Image 2' },
  { src: img3, label: 'Image 3' },
  { src: img4, label: 'Image 4' },
  { src: img5, label: 'Image 5' },
  { src: img6, label: 'Image 6' },
  { src: img7, label: 'Image 7' },
  { src: img8, label: 'Image 8' },
];

function ImageShop() {
  return (
    <Box className="main-content">
      <Typography variant="h4" gutterBottom>
        Image Store
      </Typography>
      <Grid container spacing={2}>
        {images.map((image, index) => (
          <Grid item key={index} xs={12} sm={6} md={4} lg={3}>
            <ImageCard image={image} />
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}

export default ImageShop;
