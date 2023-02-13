from views import df_concat
import sqlite3

conn = sqlite3.connect('excel_parser.sqlite')
df_concat.to_sql('excel_table', conn, if_exists='replace', index=False)
conn.commit()
conn.close()
