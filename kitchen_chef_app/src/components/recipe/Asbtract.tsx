import React, { useState } from 'react';
import Typography from '@mui/material/Typography';

const Abstract = ({ abstract }) => (
  <Typography textAlign="justify">
    {abstract}
  </Typography>
);
export default Abstract;
