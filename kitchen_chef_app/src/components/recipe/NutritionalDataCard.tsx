import React, { useState } from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { CardMedia, ToggleButton, ToggleButtonGroup } from '@mui/material';

const NutritionalDataCard = ({ nutritionalData, thumbnail }) => (
  <Card sx={{ padding: '1rem' }}>
    <Typography gutterBottom variant="h5" component="h2" noWrap>
      Nutritional Informations
    </Typography>
    <CardContent>
      <Typography gutterBottom component="div" align="left" display="flex" justifyContent="space-between">
        <span>Calories </span>
        <span>{`${nutritionalData.kcal} kCal`}</span>
      </Typography>

      <Typography gutterBottom component="div" align="left" display="flex" justifyContent="space-between">
        <span>Proteins </span>
        <span>{`${nutritionalData.proteins} g`}</span>
      </Typography>
      <Typography gutterBottom component="div" align="left" display="flex" justifyContent="space-between">
        <span>Fats </span>
        <span>{`${nutritionalData.fat} g`}</span>
      </Typography>
      <Typography gutterBottom component="div" align="left" display="flex" justifyContent="space-between">
        <span>Carbohydrates </span>
        <span>{`${nutritionalData.carbs} g`}</span>
      </Typography>
      <Typography gutterBottom component="div" align="left" display="flex" justifyContent="space-between">
        <span>Sugar </span>
        <span>{`${nutritionalData.sugar} g`}</span>
      </Typography>
      <Typography gutterBottom component="div" align="left" display="flex" justifyContent="space-between">
        <span>Fibers </span>
        <span>{`${nutritionalData.fibers} g`}</span>
      </Typography>
    </CardContent>
  </Card>
);
export default NutritionalDataCard;
