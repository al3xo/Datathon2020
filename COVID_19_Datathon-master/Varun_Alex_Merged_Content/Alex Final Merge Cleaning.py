import numpy as np 
import pandas as pd 
from itertools import groupby
from collections import OrderedDict
import matplotlib.pyplot as plt 
import seaborn as sns
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression
import sqlite3 as sql

def select_k_best(df, k):
    X = df.drop(['Won'], axis=1)
    y = df['Won']
    fs = SelectKBest(score_func=f_regression, k=k)
    fs.fit_transform(X, y)
    cols = fs.get_support(indices=True)
    new_df = df.iloc[:,cols]
    new_df['Name_Index'] = df['Unnamed: 0']
    new_df['Won'] = y
    return new_df

def remove_high_correlation(df):
    correlated_features = set()
    correlation_matrix = df.drop('Won', axis=1).corr()
    for i in range(len(correlation_matrix.columns)):
        for j in range(i):
            if abs(correlation_matrix.iloc[i, j]) > 0.8:
                colname = correlation_matrix.columns[i]
                correlated_features.add(colname)
    df = df.drop(correlated_features, axis=1)
    return df

def main():
    final = pd.read_csv(r"C:\Users\dswhi\OneDrive\Documents\UW Class Work\Dubstech\Datathon 3\Datathon2020\COVID_19_Datathon-master\Varun_Alex_Merged_Content\final-merge.csv", encoding='cp1252')
    final = final.drop(['Contracted_from_which Patient_Suspected', 'Notes', 'Type_of_transmission',
     'Unnamed: 0_x', 'Unnamed: 0_y', 'Unnamed: 0.1', 'Sno', 'statecode', 'Age_Bracket'], axis=1)
    final = pd.get_dummies(final, columns=['Gender']).drop('Unnamed: 0', axis=1)

    final = final.sort_values('Date')
    final['DaysFromFirstDate'] = 0
    xs = [list(g) for k, g in groupby(final['Date'].tolist())]
    final['DaysFromFirstDate'] += np.repeat(range(len(xs)),[len(x) for x in xs])

    conn = sql.connect(':memory:')
    final.to_sql('final', conn, index=False)
    final.to_sql('state', conn, index=False)

    qry = '''
    SELECT 
    FROM final
    ORDER BY DaysFromFirstDate, State, district
    '''
    df = pd.read_sql_query(qry, conn)
    cols = list(set(df.columns)-set(['Gender_F', 'Gender_M', 'Gender_Non-Binary']))
    genders = ['Gender_F', 'Gender_M', 'Gender_Non-Binary']
    new_df = df.filter(cols)
    new_df = new_df.drop_duplicates()
    df = df.groupby(['DaysFromFirstDate','State','district'])['Gender_F', 'Gender_M', 'Gender_Non-Binary'].sum().reset_index()
    merged = df.merge(new_df, on=['DaysFromFirstDate', 'State', 'district'])
    merged.to_csv(r"C:\Users\dswhi\OneDrive\Documents\UW Class Work\Dubstech\Datathon 3\Datathon2020\COVID_19_Datathon-master\Varun_Alex_Merged_Content\final_merge_cleaned.csv", encoding="cp1252") 

if __name__=="__main__":
    main()