from views import df_db
import sqlite3

conn = sqlite3.connect('excel_parser.sqlite')
df_db.to_sql('excel_table', conn, if_exists='replace', index=False)
conn.commit()
conn.close()
