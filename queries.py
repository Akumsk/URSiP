from model import df_parsing
import pandas as pd
import numpy as np

# Result: Creating group_table_v1
df_groupe_by_date_1 = df_parsing.groupby(['date', 'type', 'data_type', ], sort='date').aggregate({'value': 'sum'})
with pd.ExcelWriter('queries\Result_Groupe_by_date_1.xlsx') as writer:
    df_groupe_by_date_1.to_excel(writer, sheet_name='Groupe_by_date')

# Result: Creating group_table_v2
df_groupe_by_date_2 = pd.pivot_table(df_parsing, values='value', index=['date', 'type'], columns=['data_type'], aggfunc=np.sum)
with pd.ExcelWriter('queries\Result_Groupe_by_date_2.xlsx') as writer:
    df_groupe_by_date_2.to_excel(writer, sheet_name='Groupe_by_date')
