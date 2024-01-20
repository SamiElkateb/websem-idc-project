import React from 'react';
import Typography from '@mui/material/Typography';

type TAbstractProps = { abstract: string };
const Abstract:React.FC<TAbstractProps> = ({ abstract }) => (
  <Typography textAlign="justify">
    {abstract}
  </Typography>
);
export default Abstract;
