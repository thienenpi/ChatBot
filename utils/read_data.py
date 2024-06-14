import pandas as pd

# measures
def get_measures() -> pd.DataFrame:
    measures = pd.read_csv('data/measures.csv')
    return measures['Measure Name'].tolist()

# tables
def get_columns() -> pd.DataFrame:
    tables = pd.read_csv('data/tables.csv')
    columns = ''

    for index, row in tables.iterrows():
        columns += row['Name'] + ', ' + row['Columns'] + '\n'

    return columns