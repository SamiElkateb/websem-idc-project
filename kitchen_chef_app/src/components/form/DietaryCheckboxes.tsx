import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import React from 'react';

const DietaryCheckboxes:React.FC = () => {
  const options = ['Vegan', 'Gluten-Free', 'Nut-Free', 'Dairy-Free'];
  return (
    <div>
      {options.map((option) => (
        <FormControlLabel control={<Checkbox />} label={option} key={option} />
      ))}
    </div>
  );
};

export default DietaryCheckboxes;
