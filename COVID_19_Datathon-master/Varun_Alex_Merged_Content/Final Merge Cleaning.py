import numpy as np 
import pandas as pd 
from itertools import groupby
from collections import OrderedDict
import matplotlib.pyplot as plt 
import seaborn as sns

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
     'Unnamed: 0_x', 'Unnamed: 0_y', 'Sno'], axis=1)
    

if __name__=="__main__":
    main()