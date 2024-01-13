import math
from typing import List, Any

import pandas as pd

def get_attr(name):
    csv = pd.read_csv('../../../data/recipes.csv')
    units = []
    for i in range(1, 19):
        col_name = name + ("0" if i<10 else "") + str(i)
        units += list(csv[col_name].unique())
    units = {str(k).lower().strip() for k in set(units)}
    units.remove('nan')
    print(units)
    pd.DataFrame(units).to_csv('../../../data/'+name.lower()+'.csv', index=False)

if __name__ == '__main__':
    get_attr('Quantity')