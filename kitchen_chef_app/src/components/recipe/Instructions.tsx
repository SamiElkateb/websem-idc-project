import React, { useState } from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import { List, ListItem, ListItemText } from '@mui/material';

const Instructions = ({ instructions }) => (
  <Card sx={{ padding: '1rem' }}>
    <Typography gutterBottom variant="h5" component="h2" noWrap>
      Instructions
    </Typography>
    <CardContent>
      <Typography gutterBottom component="div" align="left" display="flex" justifyContent="space-between">
        <List sx={{ width: '100%', maxWidth: 360, bgcolor: 'background.paper' }}>
          {instructions.split('.').filter((item) => item !== '').map((value, index) => (
            <ListItem
              key={value}
              disableGutters
              sx={{ padding: 0.5 }}
            >
              <ListItemText primary={`${(index + 1)}. ${value}`} />
            </ListItem>
          ))}
        </List>
      </Typography>
    </CardContent>
  </Card>
);
export default Instructions;
