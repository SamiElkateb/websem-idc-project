import React, { useState } from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { CardMedia, ToggleButton, ToggleButtonGroup } from '@mui/material'; import { TIngredient } from '../../models/ingredients';

const displayQuantity = (quantity: string | number) => {
  if (typeof quantity === 'string' && quantity.match('/')) {
    return (
      <>
        <sup>{quantity.split('/')[0]}</sup>
        /
        <sub>{quantity.split('/')[1]}</sub>
      </>
    );
  }
  return quantity;
};

function decimalToFraction(decimalStr: string) {
  const decimal = parseFloat(decimalStr);
  const integer = parseInt(decimalStr, 10);
  if (isNaN(decimal) || isNaN(integer)) return decimalStr;
  const epsilon = Math.abs(integer - decimal);
  if (epsilon < Number.EPSILON) return integer;
  const fractions = [2, 3, 4, 5, 6, 8];
  for (let i = 0; i < fractions.length; i += 1) {
    const fraction = fractions[i];
    const multiplied = decimal * fraction;

    if (Math.abs(multiplied - Math.round(multiplied)) < Number.EPSILON) {
      return `${Math.round(multiplied)}/${fraction}`;
    }
  }
  if (Number.isNaN(decimalStr)) return decimalStr;
  return Math.round(parseFloat(decimalStr) * 100) / 100;
}

type TIngredientsCardProps = { ingredients: TIngredient[];
  thumbnail: string };
const IngredientsCard:React.FC<TIngredientsCardProps> = ({ ingredients, thumbnail }) => {
  const [unitSystem, setUnitSystem] = useState<'imperial' | 'metric'>('imperial');
  const handleUnitSystemChange = (
    _: React.MouseEvent<HTMLElement>,
    newUnitSystem: string,
  ) => {
    if (newUnitSystem !== 'imperial' && newUnitSystem !== 'metric') return;
    setUnitSystem(newUnitSystem);
  };
  return (
    <Card sx={{ backgroundColor: '#f4f4f3', flex: '1' }}>
      {
        thumbnail ? (
          <CardMedia
            sx={{ height: 140 }}
            image={thumbnail}
          />
        ) : null
      }
      <CardContent sx={{ padding: '1.5rem 1rem' }}>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Typography
            gutterBottom
            variant="h5"
            component="h2"
            noWrap
            textAlign="left"
            color="#5c6165"
            sx={{ textTransform: 'uppercase' }}
          >
            Ingredients
          </Typography>
          <ToggleButtonGroup
            value={unitSystem}
            exclusive
            onChange={handleUnitSystemChange}
            aria-label="unit system"
          >
            <ToggleButton value="imperial" aria-label="imperial">
              US
            </ToggleButton>
            <ToggleButton value="metric" aria-label="metric">
              METRIC
            </ToggleButton>
          </ToggleButtonGroup>
        </Box>
        {ingredients.map((item) => (
          <Typography gutterBottom component="div" align="left" display="flex" alignItems="center">
            <Box component="span" fontSize="1.5rem" marginRight="0.5rem">
              {displayQuantity(decimalToFraction(item[`${unitSystem}Measure`].quantity))}
            </Box>
            <Box component="span" sx={{ verticalAlign: 'top' }}>
              {` ${item[`${unitSystem}Measure`].unit} ${item.name}`}
            </Box>
          </Typography>

        ))}
      </CardContent>
    </Card>
  );
};
export default IngredientsCard;
