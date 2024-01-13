import React from 'react';
import Chip from '@mui/material/Chip';
import { TIngredient } from '../../models/ingredients';
import { TFilter } from '../../models/others';

type FiltersProps = {
  filters: TFilter[]
  ingredients?: TIngredient[]
  onDeactiveFilter: (item: TFilter) => void
  onActivateFilter: (item: TFilter) => void
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
        key={item.id}
        label={item.frLabel}
        onDelete={() => onRemoveIngredient(item.id)}
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