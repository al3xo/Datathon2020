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

def censusMerger(district, state):
    state.columns = [c.replace(' ', '_') for c in state.columns]
    state.columns = [c.replace('/', '') for c in state.columns]
    district.columns = [c.replace(' ', '_') for c in district.columns]

    conn = sql.connect(':memory:')
    district.to_sql('district', conn, index=False)
    state.to_sql('state', conn, index=False)

    qry = '''
    SELECT *
    FROM state join district on LOWER(state.State__Union_Territory) = LOWER(district.State_name)
    '''
    df = pd.read_sql_query(qry, conn)
    df.to_csv(r"C:\Users\Alex Omusoru\Documents\GitHub\Datathon2020\COVID_19_Datathon-master\Varun_Alex_Merged_Content\census_merge.csv", encoding="cp1252")
    

def main():
    patient_city_district_may_5_refined = pd.read_csv(r"C:\Users\Alex Omusoru\Documents\GitHub\Datathon2020\COVID_19_Datathon-master\Varun_Preprocessed_Data1\patient-city-district-refined.csv")
    districts_daily_refined = pd.read_csv(r"C:\Users\Alex Omusoru\Documents\GitHub\Datathon2020\COVID_19_Datathon-master\Varun_Preprocessed_Data1\districts-daily-refined.csv")
    statewise_testing_refined = pd.read_csv(r"C:\Users\Alex Omusoru\Documents\GitHub\Datathon2020\COVID_19_Datathon-master\Varun_Preprocessed_Data1\statewise-testing-refined.csv")
    zones_refined = pd.read_csv(r"C:\Users\Alex Omusoru\Documents\GitHub\Datathon2020\COVID_19_Datathon-master\Varun_Preprocessed_Data1\zones-refined.csv")
    
    hospital_beds = pd.read_csv(r"C:\Users\Alex Omusoru\Documents\GitHub\Datathon2020\COVID_19_Datathon-master\additional_data\HospitalBedsIndia.csv")
    icmr = pd.read_csv(r"C:\Users\Alex Omusoru\Documents\GitHub\Datathon2020\COVID_19_Datathon-master\additional_data\ICMRTestingLabs.csv")
    district_census = pd.read_csv(r"C:\Users\Alex Omusoru\Documents\GitHub\Datathon2020\COVID_19_Datathon-master\additional_data\district_population_india_census2011.csv")
    state_census = pd.read_csv(r"C:\Users\Alex Omusoru\Documents\GitHub\Datathon2020\COVID_19_Datathon-master\additional_data\state_population_india_census2011.csv")

    # print(patient_city_district_may_5_refined.columns) #Date_Announced, City, District, State
    # print(districts_daily_refined.columns) #State, district, date
    # print(statewise_testing_refined.columns) #Date, State
    # print(zones_refined.columns) #district, state, zone
    # print(hospital_beds.columns) #state
    # print(icmr.columns) #city, state
    # print(district_census.columns) #district, state
    # print(state_census.columns) #State / Union Territory
    
    censusMerger(district_census,state_census)

if __name__=="__main__":
    main()