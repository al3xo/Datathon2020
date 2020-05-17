import numpy as np 
import pandas as pd 
from itertools import groupby
from collections import OrderedDict
import matplotlib.pyplot as plt 
import seaborn as sns
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression
import sqlite3

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

def merge_dfs(patient, district, statewise_testing, zones, hospital_beds, icmr, district_census, state_census):
    merged = patient.merge(district, left_on=['Date_Announced', 'Detected_District', 'Detected_State', 'DaysFromFirstDate'], right_on=['date', 'district', 'State', 'DaysFromFirstDate'])
    merged = merged.drop(['Detected_City', 'Date_Announced', 'Detected_District', 'Detected_State'], axis=1)
    nas = merged['Age_Bracket'].ne('Unknown') & merged['Gender'].ne('Unknown')
    merged = merged[nas]
    merged = merged.merge(statewise_testing, left_on=['date', 'State'], right_on=['Date', 'State']).drop('date', axis=1)
    merged = merged.merge(zones, left_on=['district', 'State'], right_on=['district', 'state']).drop('state', axis=1)
    merged = merged.merge(hospital_beds, left_on='State', right_on='State/UT', how='left').drop('State/UT', axis=1)
    bed_cols = ['NumPrimaryHealthCenters_HMIS', 'NumCommunityHealthCenters_HMIS',
     'NumSubDistrictHospitals_HMIS', 'NumDistrictHospitals_HMIS', 'TotalPublicHealthFacilities_HMIS',
     'NumPublicBeds_HMIS', 'NumRuralHospitals_NHP18', 'NumRuralBeds_NHP18', 'NumUrbanHospitals_NHP18',
     'NumUrbanBeds_NHP18']
    merged[bed_cols] = merged[bed_cols].fillna(0)
    merged = merged.merge(icmr, left_on='State', right_on='state').drop('state', axis=1)
    return merged

def merge_census(merged, census):
    new_merge = merged.merge(census, left_on=['State', 'district'], right_on=['State', 'District_name']).drop('District_name', axis=1)
    return new_merge

def main():
    patient_city_district_may_5_refined = pd.read_csv(r"C:\Users\dswhi\OneDrive\Documents\UW Class Work\Dubstech\Datathon 3\Datathon2020\COVID_19_Datathon-master\Varun_Preprocessed_Data1\patient-city-district-refined.csv").drop('Unnamed: 0', axis=1)
    districts_daily_refined = pd.read_csv(r"C:\Users\dswhi\OneDrive\Documents\UW Class Work\Dubstech\Datathon 3\Datathon2020\COVID_19_Datathon-master\Varun_Preprocessed_Data1\districts-daily-refined.csv").drop('Unnamed: 0', axis=1)
    statewise_testing_refined = pd.read_csv(r"C:\Users\dswhi\OneDrive\Documents\UW Class Work\Dubstech\Datathon 3\Datathon2020\COVID_19_Datathon-master\Varun_Preprocessed_Data1\statewise-testing-refined.csv")
    zones_refined = pd.read_csv(r"C:\Users\dswhi\OneDrive\Documents\UW Class Work\Dubstech\Datathon 3\Datathon2020\COVID_19_Datathon-master\Varun_Preprocessed_Data1\zones-refined.csv")
    
    hospital_beds = pd.read_csv(r"C:\Users\dswhi\OneDrive\Documents\UW Class Work\Dubstech\Datathon 3\Datathon2020\COVID_19_Datathon-master\additional_data\HospitalBedsIndia.csv")
    icmr = pd.read_csv(r"C:\Users\dswhi\OneDrive\Documents\UW Class Work\Dubstech\Datathon 3\Datathon2020\COVID_19_Datathon-master\Varun_Preprocessed_Data1\icmr-refined.csv")
    district_census = pd.read_csv(r"C:\Users\dswhi\OneDrive\Documents\UW Class Work\Dubstech\Datathon 3\Datathon2020\COVID_19_Datathon-master\additional_data\district_population_india_census2011.csv")
    state_census = pd.read_csv(r"C:\Users\dswhi\OneDrive\Documents\UW Class Work\Dubstech\Datathon 3\Datathon2020\COVID_19_Datathon-master\additional_data\state_population_india_census2011.csv")
    merged = merge_dfs(patient_city_district_may_5_refined, districts_daily_refined, statewise_testing_refined,
     zones_refined, hospital_beds, icmr, district_census, state_census)
    #merged.to_csv(r"C:\Users\dswhi\OneDrive\Documents\UW Class Work\Dubstech\Datathon 3\Datathon2020\COVID_19_Datathon-master\Varun_Alex_Merged_Content\patient-to-icmr-merge.csv")
    census = pd.read_csv(r"C:\Users\dswhi\OneDrive\Documents\UW Class Work\Dubstech\Datathon 3\Datathon2020\COVID_19_Datathon-master\Varun_Alex_Merged_Content\census_merge.csv", encoding="cp1252")
    census = census.drop(['Sno', 'State_name'], axis=1)
    census = census.rename(columns={'State__Union_Territory':'State'})
    new_merge = merge_census(merged, census) 
    new_merge.to_csv(r"C:\Users\dswhi\OneDrive\Documents\UW Class Work\Dubstech\Datathon 3\Datathon2020\COVID_19_Datathon-master\Varun_Alex_Merged_Content\final-merge.csv", encoding="cp1252")

if __name__=="__main__":
    main()