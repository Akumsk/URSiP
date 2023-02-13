import pandas as pd
from views import parsing_excel_3groups
import sqlite3

path = 'sources'
file_name = 'Приложение к заданию бек разработчика.xlsx'
df = pd.read_excel(path + r'/' + file_name, header=None)
df_parsing = parsing_excel_3groups(df)

conn = sqlite3.connect('excel_parser.sqlite')
df_parsing.to_sql('excel_table', conn, if_exists='replace', index=False)
conn.commit()
conn.close()
