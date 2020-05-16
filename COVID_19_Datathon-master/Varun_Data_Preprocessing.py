import numpy as np 
import pandas as pd 
from itertools import groupby
from collections import OrderedDict

def refine_state_wise(df):
    #Confirmed-1, Deceased-2, Recovered-3
    df['Status'] = df['Status'].replace(['Confirmed', 'Deceased','Recovered'], [1, 2, 3])
    return df

def refine_patient_city_district(df):
    df = df.drop(['Source_1', 'Source_2', 'Source_3'], axis=1)
    return df

def refine_districts_daily(df):
    df = df.sort_values(['date', 'State', 'district'])
    return df

def refine_statewise_testing(df):
    df['Negative'] = df['Negative'].fillna(method='ffill')
    samples_dont_add = (df['Negative']+df['Positive']) > df['TotalSamples']
    df.loc[samples_dont_add, 'Negative'] = df['Negative']- (df['Negative']+df['Positive']-df['TotalSamples'])
    return df

def refine_zones(df):
    #Green-1, Orange-2, Red-3
    df['zone'] = df['zone'].replace(['Green', 'Orange','Red'], [1, 2, 3])
    df = df.drop(['districtcode', 'lastupdated', 'source'], axis=1)
    return df

def combine_dates(districts, patients, state_wise_daily, statewise_testing, zones):
    date1 = districts['date'].to_frame()
    date2 = patients['Date_Announced'].to_frame()
    date3 = state_wise_daily['Date'].to_frame()
    date4 = statewise_testing['Date'].to_frame()
    grouped = pd.concat([date1, date2, date3, date4], ignore_index=True)
    grouped = grouped.fillna('')
    grouped['Date'] = grouped['Date'] + grouped['Date_Announced'] + grouped['date']
    grouped = grouped['Date'].to_frame().sort_values('Date')
    grouped = grouped.drop_duplicates()
    grouped['DaysFromFirstDate'] = 0
    xs = [list(g) for k, g in groupby(grouped['Date'].tolist())]
    grouped['DaysFromFirstDate'] += np.repeat(range(len(xs)),[len(x) for x in xs])
    return grouped

def combine_dates(districts, patients, state_wise_daily, statewise_testing):
    date1 = districts['date'].to_frame()
    date2 = patients['Date_Announced'].to_frame()
    date3 = state_wise_daily['Date'].to_frame()
    date4 = statewise_testing['Date'].to_frame()
    grouped = pd.concat([date1, date2, date3, date4], ignore_index=True)
    grouped = grouped.fillna('')
    grouped['Date'] = grouped['Date'] + grouped['Date_Announced'] + grouped['date']
    grouped = grouped['Date'].to_frame().sort_values('Date')
    grouped = grouped.drop_duplicates()
    grouped['DaysFromFirstDate'] = 0
    xs = [list(g) for k, g in groupby(grouped['Date'].tolist())]
    grouped['DaysFromFirstDate'] += np.repeat(range(len(xs)),[len(x) for x in xs])
    districts = districts.merge(grouped, left_on='date', right_on='Date').drop('Date', axis=1)
    patients = patients.merge(grouped, left_on='Date_Announced', right_on='Date').drop('Date', axis=1)
    state_wise_daily = state_wise_daily.merge(grouped, on='Date')
    statewise_testing = statewise_testing.merge(grouped, on='Date')
    return districts, patients, state_wise_daily, statewise_testing

def main():
    state_wise_daily = pd.read_csv(r"C:\Users\dswhi\OneDrive\Documents\UW Class Work\Dubstech\Datathon 3\Datathon2020\COVID_19_Datathon-master\state_wise_daily_delhi_gujurat_maharashtra_tamil_nadu_may_15_2020 - state_wise_daily_mh_gj_dl_tn.csv")
    state_wise_daily_refined = refine_state_wise(state_wise_daily)

    patient_city_district_may_5 = pd.read_csv(r"C:\Users\dswhi\OneDrive\Documents\UW Class Work\Dubstech\Datathon 3\Datathon2020\COVID_19_Datathon-master\patient_city_district_wise_data_may_5_date_formatted.csv")
    patient_city_district_may_5_refined = refine_patient_city_district(patient_city_district_may_5)

    districts_daily = pd.read_csv(r"C:\Users\dswhi\OneDrive\Documents\UW Class Work\Dubstech\Datathon 3\Datathon2020\COVID_19_Datathon-master\districts_daily_may_15.csv")
    districts_daily_refined = refine_districts_daily(districts_daily)

    statewise_testing = pd.read_csv(r"C:\Users\dswhi\OneDrive\Documents\UW Class Work\Dubstech\Datathon 3\Datathon2020\COVID_19_Datathon-master\additional_data\StatewiseTestingDetails.csv")
    statewise_testing_refined = refine_statewise_testing(statewise_testing)

    zones = pd.read_csv(r"C:\Users\dswhi\OneDrive\Documents\UW Class Work\Dubstech\Datathon 3\Datathon2020\COVID_19_Datathon-master\additional_data\zones.csv")
    zones_refined = refine_zones(zones)

    districts_daily_refined, patient_city_district_may_5_refined, state_wise_daily_refined, statewise_testing_refined = combine_dates(districts_daily_refined, patient_city_district_may_5_refined, state_wise_daily_refined, statewise_testing_refined)

    state_wise_daily_refined.to_csv(r"C:\Users\dswhi\OneDrive\Documents\UW Class Work\Dubstech\Datathon 3\Datathon2020\COVID_19_Datathon-master\Varun_Preprocessed_Data1\state-wise-daily-refined.csv")
    patient_city_district_may_5_refined.to_csv(r"C:\Users\dswhi\OneDrive\Documents\UW Class Work\Dubstech\Datathon 3\Datathon2020\COVID_19_Datathon-master\Varun_Preprocessed_Data1\patient-city-district-refined.csv")
    districts_daily_refined.to_csv(r"C:\Users\dswhi\OneDrive\Documents\UW Class Work\Dubstech\Datathon 3\Datathon2020\COVID_19_Datathon-master\Varun_Preprocessed_Data1\districts-daily-refined.csv")
    statewise_testing_refined.to_csv(r"C:\Users\dswhi\OneDrive\Documents\UW Class Work\Dubstech\Datathon 3\Datathon2020\COVID_19_Datathon-master\Varun_Preprocessed_Data1\statewise-testing-refined.csv")
    zones_refined.to_csv(r"C:\Users\dswhi\OneDrive\Documents\UW Class Work\Dubstech\Datathon 3\Datathon2020\COVID_19_Datathon-master\Varun_Preprocessed_Data1\zones-refined.csv")

if __name__ == "__main__":
    main()