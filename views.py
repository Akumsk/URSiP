import pandas as pd
import numpy as np
from datetime import datetime

df_excel = pd.read_excel('sources/Приложение к заданию бек разработчика.xlsx', header=None)

# Input data, can optimizing with Unique()
name_col_1 = df_excel[0][0]  # id
name_col_2 = df_excel[1][0]  # company
name_group_1 = 'status'
value_1_groupe_1 = df_excel[2][0]  # fact
value_2_groupe_1 = df_excel[6][0]  # forecast

name_group_2 = 'type'
value_1_groupe_2 = df_excel[2][1]  # Qliq
value_2_groupe_2 = df_excel[4][1]  # Qoil

name_group_3 = 'data_type'
value_1_groupe_3 = df_excel[2][2]  # data1
value_2_groupe_3 = df_excel[3][2]  # data2

# Fill Groupe-Headers
list_name_collumns = [''.join(df_excel[0][0:3].fillna(''))]
for column in range(1, len(df_excel.columns)):
    df_excel[column][0:3] = df_excel[column][0:3].fillna(df_excel[column - 1][0:3])
    list_name_collumns.append(''.join(df_excel[column][0:3].fillna('')))

# Rename columns
df_excel.columns = list_name_collumns

# Add dates
df_excel['date'] = ['2022-01-01', '2022-01-05', '2022-01-10', '2022-01-15', '2022-01-01',
                    '2022-01-05', '2022-01-10', '2022-01-15', '2022-01-30', '2022-01-25',
                    '2022-01-01', '2022-01-12', '2022-01-10', '2022-01-15', '2022-01-01',
                    '2022-01-01', '2022-01-07', '2022-01-18', '2022-01-17', '2022-01-02',
                    '2022-01-18', '2022-01-17', '2022-01-02']
df_excel['date'] = df_excel['date'].apply(
    lambda x: datetime.strptime(x, '%Y-%m-%d'))

##Separating origin Excel table to DF, match by groups, concat to DB-table
dict_df_concat = dict.fromkeys(df_excel.columns)

# Fill Groupe-Column according ExcelGroupe
for column in dict_df_concat:
    if (value_1_groupe_1 in column
            or value_2_groupe_1 in column
            or value_1_groupe_2 in column
            or value_2_groupe_2 in column):
        dict_df_concat[column] = df_excel.loc[:][column].to_frame()
        dict_df_concat[column][name_col_1] = df_excel.loc[:][name_col_1]
        dict_df_concat[column][name_col_2] = df_excel.iloc[:][name_col_2]
        dict_df_concat[column]['date'] = df_excel.loc[:]['date']
        dict_df_concat[column][name_group_2] = dict_df_concat[column].loc[1][column]
        dict_df_concat[column][name_group_1] = dict_df_concat[column].loc[0][column]
        dict_df_concat[column][name_group_3] = dict_df_concat[column].iloc[2][column]
        dict_df_concat[column].rename(columns={column: dict_df_concat[column].iloc[2][column]}, inplace=True)
        dict_df_concat[column].columns = dict_df_concat[column].columns.str.replace(value_1_groupe_3, 'value')
        dict_df_concat[column].columns = dict_df_concat[column].columns.str.replace(value_2_groupe_3, 'value')
        dict_df_concat[column] = dict_df_concat[column].drop([0, 1, 2])

# Concat df to DB table
df_concat = dict_df_concat[''.join([value_1_groupe_1, value_1_groupe_2, value_1_groupe_3])]
for dict_key in dict_df_concat.keys():
    if (value_1_groupe_1 in dict_key
            or value_2_groupe_1 in dict_key
            or value_1_groupe_2 in dict_key
            or value_2_groupe_2 in dict_key):
        if dict_key == ''.join([value_1_groupe_1, value_1_groupe_2, value_1_groupe_3]):
            continue
        df_concat = df_concat.merge(dict_df_concat[dict_key], how='outer')

df_concat = df_concat[['id', 'company', 'date', 'type', 'status', 'data_type', 'value']]

#Define/check type of collumns
df_concat.id = df_concat.id.astype(int)
df_concat.company = df_concat.company.astype(str)
df_concat.type = df_concat.type.astype(str)
df_concat.status = df_concat.status.astype(str)
df_concat.data_type = df_concat.data_type.astype(str)
df_concat.value = df_concat.value.astype(int)

#Result: Creating group_table_v1
df_groupe_by_date_1 = df_concat.groupby(['date', 'type', 'data_type', ], sort = 'date').aggregate({'value': 'sum'})
with pd.ExcelWriter('queries\Result_Groupe_by_date_1.xlsx') as writer:
    df_groupe_by_date_1.to_excel(writer, sheet_name='Groupe_by_date')

#Result: Creating group_table_v2
df_groupe_by_date_2 = pd.pivot_table(df_concat, values='value', index=['date', 'type'], columns=['data_type'], aggfunc=np.sum)
with pd.ExcelWriter('queries\Result_Groupe_by_date_2.xlsx') as writer:
    df_groupe_by_date_2.to_excel(writer, sheet_name='Groupe_by_date')
