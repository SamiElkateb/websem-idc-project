import React from 'react';
import Chip from '@mui/material/Chip';

type FiltersProps = {
  filters: { name: string, active: boolean }[]
  ingredients?: string[]
  onDeactiveFilter: (item: string) => void
  onActivateFilter: (item: string) => void
  onRemoveIngredient : (item: string) => void
};

const Filters:React.FC<FiltersProps> = ({
  filters,
  ingredients,
  onDeactiveFilter,
  onActivateFilter,
  onRemoveIngredient,
}) => (
  <div>
    {filters!.map((item) => (
      item.active
        ? (
          <Chip
            key={item.name}
            label={item.name}
            onDelete={() => onDeactiveFilter(item)}
            style={{ margin: '5px' }}
            color="primary"
          />
        ) : (
          <Chip
            key={item.name}
            label={item.name}
            onClick={() => onActivateFilter(item)}
            style={{ margin: '5px' }}
          />
        )
    ))}
    {ingredients!.map((item) => (
      <Chip
        key={item}
        label={item}
        onDelete={() => onRemoveIngredient(item)}
        style={{ margin: '5px' }}
        color="primary"
      />
    ))}
  </div>
);

Filters.defaultProps = {
  ingredients: [],

};

export default Filters;
