import numpy as np 
import pandas as pd 
from itertools import groupby
from collections import OrderedDict
import sqlite3 as sql

def main():
    final = pd.read_csv(r"C:\Users\dswhi\OneDrive\Documents\UW Class Work\Dubstech\Datathon 3\Datathon2020\COVID_19_Datathon-master\Varun_Alex_Merged_Content\final-merge.csv", encoding='cp1252')
    final = final.drop(['Contracted_from_which Patient_Suspected', 'Notes', 'Type_of_transmission',
     'Unnamed: 0_x', 'Unnamed: 0_y', 'Unnamed: 0.1', 'Sno', 'statecode', 'State_Code', 'Age_Bracket'], axis=1)
    final = pd.get_dummies(final, columns=['Gender']).drop('Unnamed: 0', axis=1)
    final['Density'] = final['Density'].str.split('/').str[0]
    final['Area'] = final['Area'].str.split().str[0]

    final = final.sort_values('Date')
    final['DaysFromFirstDate'] = 0
    xs = [list(g) for k, g in groupby(final['Date'].tolist())]
    final['DaysFromFirstDate'] += np.repeat(range(len(xs)),[len(x) for x in xs])

    conn = sql.connect(':memory:')
    final.to_sql('final', conn, index=False)

    qry = '''
    SELECT *
    FROM final
    ORDER BY DaysFromFirstDate, State, district
    '''
    df = pd.read_sql_query(qry, conn)
    cols = list(set(df.columns)-set(['Gender_F', 'Gender_M', 'Gender_Non-Binary']))
    genders = ['Gender_F', 'Gender_M', 'Gender_Non-Binary']
    new_df = df.filter(cols)
    new_df = new_df.drop_duplicates()
    df = df.groupby(['DaysFromFirstDate','State','district'])['Gender_F', 'Gender_M', 'Gender_Non-Binary'].sum().reset_index()
    merged = df.merge(new_df, on=['DaysFromFirstDate', 'State', 'district']).drop(['Date', 'Nationality'], axis=1)
    merged.to_csv(r"C:\Users\dswhi\OneDrive\Documents\UW Class Work\Dubstech\Datathon 3\Datathon2020\COVID_19_Datathon-master\Varun_Alex_Merged_Content\final_merge_cleaned.csv", encoding="cp1252")

    with_state_totals = pd.read_csv(r"C:\Users\dswhi\OneDrive\Documents\UW Class Work\Dubstech\Datathon 3\Datathon2020\COVID_19_Datathon-master\Varun_Alex_Merged_Content\final_plus_state.csv")
    districts = ['Mumbai', 'Delhi', 'Ahmedabad', 'Chennai']
    states = ['Maharashtra', 'Delhi', 'Tamil Nadu', 'Gujarat']
    instate = with_state_totals['State'].isin(states)
    indist = with_state_totals['district'].isin(districts)
    states_df = with_state_totals[instate]
    dist_df = with_state_totals[indist]
    states_df.to_csv(r"C:\Users\dswhi\OneDrive\Documents\UW Class Work\Dubstech\Datathon 3\Datathon2020\COVID_19_Datathon-master\Varun_Alex_Merged_Content\4-states-only.csv")
    dist_df.to_csv(r"C:\Users\dswhi\OneDrive\Documents\UW Class Work\Dubstech\Datathon 3\Datathon2020\COVID_19_Datathon-master\Varun_Alex_Merged_Content\4-districts-only.csv")

if __name__=="__main__":
    main()