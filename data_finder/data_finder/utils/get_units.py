import pandas as pd

if __name__ == '__main__':
    csv = pd.read_csv('../../../data/recipes.csv')
    col_name = "Unit"
    units = []
    for i in range(1, 19):
        col_name = "Unit" + ("0" if i<10 else "") + str(i)
        units += list(csv[col_name].unique())
    units = {str(k).lower().strip() for k in set(units)}
    print(units)
    pd.DataFrame(units).to_csv('../../../data/units.csv', index=False)