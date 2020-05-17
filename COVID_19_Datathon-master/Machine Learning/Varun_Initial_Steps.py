import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.linear_model import LassoCV
from sklearn.linear_model import ElasticNetCV
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score

def select_k_best(df, k):
    X = df.drop(['Positive'], axis=1)
    y = df['Positive']
    fs = SelectKBest(score_func=f_regression, k=k)
    fs.fit_transform(X, y)
    cols = fs.get_support(indices=True)
    new_df = df.iloc[:,cols]
    new_df['Positive'] = y
    return new_df

def remove_high_correlation(df):
    correlated_features = set()
    correlation_matrix = df.drop('Positive', axis=1).corr()
    for i in range(len(correlation_matrix.columns)):
        for j in range(i):
            if abs(correlation_matrix.iloc[i, j]) > 0.8:
                colname = correlation_matrix.columns[i]
                correlated_features.add(colname)
    df = df.drop(correlated_features, axis=1)
    return df

def model(df):
    k_val = 40
    df = pd.get_dummies(df)
    df = remove_high_correlation(df)
    df = select_k_best(df, k_val)
    X = df.drop('Positive', axis=1)
    y = df['Positive']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=42)
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.fit_transform(X_test)
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    lr_pred = lr.predict(X_test)
    print('Linear Regression: ' + str(k_val))
    print(mean_squared_error(y_test, lr_pred))
    print(lr.score(X_test, y_test))
    scores = cross_val_score(lr, X_train, y_train, cv=20)
    print(scores)
    print(scores.mean())

def svr(df):
    k_val = 70
    df = pd.get_dummies(df)
    df = remove_high_correlation(df)
    df = select_k_best(df, k_val)
    X = df.drop('Positive', axis=1)
    y = df['Positive']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=42)
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.fit_transform(X_test)
    clf = SVR(kernel='linear', C=1)
    clf.fit(X_train, y_train)
    pred = clf.predict(X_test)
    print('SVR: ' + str(k_val))
    print(mean_squared_error(y_test, pred))
    print(clf.score(X_test, y_test))

def lasso_cv(df):
    k_val = 40
    df = pd.get_dummies(df)
    df = remove_high_correlation(df)
    df = select_k_best(df, k_val)
    X = df.drop('Positive', axis=1)
    y = df['Positive']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=42)
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.fit_transform(X_test)
    lasso = LassoCV(cv=20, tol=.01)
    lasso.fit(X_train, y_train)
    pred = lasso.predict(X_test)
    print('LassoCV Regression: ' + str(k_val))
    print(mean_squared_error(y_test, pred))
    print(lasso.score(X_test, y_test))
    scores = cross_val_score(lasso, X_train, y_train, cv=20)
    print(scores)
    print(scores.mean())

def elastic_net(df):
    k_val = 50
    df = pd.get_dummies(df)
    df = remove_high_correlation(df)
    df = select_k_best(df, k_val)
    X = df.drop('Positive', axis=1)
    y = df['Positive']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=42)
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.fit_transform(X_test)
    en = ElasticNetCV(cv=20, tol=.01)
    en.fit(X_train, y_train)
    pred = en.predict(X_test)
    print('LassoCV Regression: ' + str(k_val))
    print(mean_squared_error(y_test, pred))
    print(en.score(X_test, y_test))
    scores = cross_val_score(en, X_train, y_train, cv=20)
    print(scores)
    print(scores.mean())

def main():
    #40 seems to be the general highest accuracy for k best
    df = pd.read_csv(r"C:\Users\dswhi\OneDrive\Documents\UW Class Work\Dubstech\Datathon 3\Datathon2020\COVID_19_Datathon-master\Varun_Alex_Merged_Content\final_merge_cleaned.csv") 
    #svr(df) # - not very accurate. Around 30%
    #model(df) # - fairly accurate. Common and averages around 70%
    #lasso_cv(df) # - fairly accurate. Common and averages around 70% with default CV and manual CV
    #elastic_net(df) # - not as accurate. Commonly around 60% but averages show to be closer to 45%

if __name__=="__main__":
    main()
