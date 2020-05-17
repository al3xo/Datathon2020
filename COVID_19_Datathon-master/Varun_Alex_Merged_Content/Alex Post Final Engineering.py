import numpy as np 
import pandas as pd 
from itertools import groupby
from collections import OrderedDict
import sqlite3 as sql

def main():
    final = pd.read_csv(r"C:\Users\Alex Omusoru\Documents\GitHub\Datathon2020\COVID_19_Datathon-master\Varun_Alex_Merged_Content\final_merge_cleaned.csv", encoding='cp1252')

    conn = sql.connect(':memory:')
    final.to_sql('final', conn, index=False)

    qry = '''
    WITH stateStats AS(
        SELECT DaysFromFirstDate as dffd, State as st, SUM(active) state_active, SUM(recovered) state_recovered, SUM(deceased) state_deceased
        FROM final
        GROUP BY DaysFromFirstDate, State
    )

    SELECT * FROM final f, stateStats ss
    WHERE f.State = ss.st
    AND ss.dffd = f.DaysFromFirstDate
    '''
    df = pd.read_sql_query(qry, conn)

    df = df.drop(['Unnamed: 0','dffd','st'], axis=1)
    df.to_csv(r"C:\Users\Alex Omusoru\Documents\GitHub\Datathon2020\COVID_19_Datathon-master\Varun_Alex_Merged_Content\final_plus_state.csv", encoding="cp1252") 

    qry2= '''
    
    SELECT DaysFromFirstDate as dffd, State as st, SUM(active) state_active, SUM(recovered) state_recovered, SUM(deceased) state_deceased
    FROM final
    GROUP BY DaysFromFirstDate, State
    
    '''
    df2 = pd.read_sql_query(qry2, conn)

    df2.to_csv(r"C:\Users\Alex Omusoru\Documents\GitHub\Datathon2020\COVID_19_Datathon-master\Varun_Alex_Merged_Content\states_act_rec_dec.csv", encoding="cp1252") 

if __name__=="__main__":
    main()