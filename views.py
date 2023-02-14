import pandas as pd
import numpy as np
from datetime import datetime


def add_date(df_excel, lst):
    df_excel[len(df_excel.columns)] = (['date', '', ''] + lst)
    return df_excel


def parsing_excel_3groups(df_excel): # Should divide on several def
    # Input data
    name_col_1 = df_excel[0][0]  # id
    name_col_2 = df_excel[1][0]  # company
    name_group_1 = 'status'
    value_1_groupe_1 = df_excel[2][0]  # fact, ##can optimize with Unique()
    value_2_groupe_1 = df_excel[6][0]  # forecast, ##can optimize with Unique()

    name_group_2 = 'type'
    value_1_groupe_2 = df_excel[2][1]  # Qliq, ##can optimize with Unique()
    value_2_groupe_2 = df_excel[4][1]  # Qoil, ##can optimize with Unique()

    name_group_3 = 'data_type'
    value_1_groupe_3 = df_excel[2][2]  # data1
    value_2_groupe_3 = df_excel[3][2]  # data2

    # Fill Group-Headers
    list_name_collumns = [''.join(df_excel[0][0:3].fillna(''))]
    for column in range(1, len(df_excel.columns)):
        df_excel[column][0:3] = df_excel[column][0:3].fillna(df_excel[column - 1][0:3])
        list_name_collumns.append(''.join(df_excel[column][0:3].fillna('')))

    # Rename columns
    df_excel.columns = list_name_collumns

    ##Separating origin Excel table to DF, match by groups
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
    df_db = dict_df_concat[''.join([value_1_groupe_1, value_1_groupe_2, value_1_groupe_3])]
    for dict_key in dict_df_concat.keys():
        if (value_1_groupe_1 in dict_key
                or value_2_groupe_1 in dict_key
                or value_1_groupe_2 in dict_key
                or value_2_groupe_2 in dict_key):
            if dict_key == ''.join([value_1_groupe_1, value_1_groupe_2, value_1_groupe_3]):
                continue
            df_db = df_db.merge(dict_df_concat[dict_key], how='outer')

    # Finally renaming df
    df_db = df_db[['id', 'company', 'date', 'type', 'status', 'data_type', 'value']]

    # Define/check type of collumns
    df_db.id = df_db.id.astype(int)
    df_db.company = df_db.company.astype(str)
    df_db.type = df_db.type.astype(str)
    df_db.status = df_db.status.astype(str)
    df_db.data_type = df_db.data_type.astype(str)
    df_db.value = df_db.value.astype(int)

    # Add uniq ID to index
    df_db.reset_index(inplace=True)

    return df_db
