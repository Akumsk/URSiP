import pandas as pd
from views import parsing_excel_3groups, add_date
import sqlite3

# Loading excel
path = 'sources'
file_name = 'Приложение к заданию бек разработчика.xlsx'
df = pd.read_excel(path + r'/' + file_name, header=None)

# Define dates
dates = ['15/01/2022', '10/01/2022', '18/01/2022', '22/01/2022', '11/01/2022', '15/01/2022', '26/01/2022',
         '18/01/2022', '11/01/2022', '23/01/2022', '01/01/2022', '08/01/2022', '15/01/2022', '17/01/2022',
         '24/01/2022', '30/01/2022', '27/01/2022',
         '17/01/2022', '11/01/2022', '25/01/2022']
df = add_date(df, dates)

# Parsing excel
df_parsing = parsing_excel_3groups(df)

# Connect to DB
conn = sqlite3.connect('excel_parser.sqlite')
df_parsing.to_sql('excel_table', conn, if_exists='replace', index=False)
conn.commit()
conn.close()
