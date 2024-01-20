import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';

import { Link } from 'react-router-dom';

type TRecipeCardProps = {
  title: string;
  description: string;
  thumbnail: string;
  uri: string;
};
const RecipeCard:React.FC<TRecipeCardProps> = ({
  title, description, thumbnail, uri,
}) => {
  const image = thumbnail || 'https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg';
  return (
    <Link
      to={`/recipes/${encodeURIComponent(uri)}`}
      style={{
        textDecoration: 'none',
      }}
    >
      <Card sx={{
        maxWidth: 345,
      }}
      >
        <CardMedia
          sx={{
            height: 140,
          }}
          image={image}
          title={title}
        />
        <CardContent>
          <Typography gutterBottom variant="h6" component="div" noWrap>
            {title}
          </Typography>
          <Typography
            variant="body2"
            color="text.secondary"
            noWrap
          >
            {description}
          </Typography>
        </CardContent>
      </Card>
    </Link>
  );
};
export default RecipeCard;
