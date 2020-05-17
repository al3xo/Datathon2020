# Datathon2020

### Visualizations:
The first links contains two visualizations that show the growth and spread of COVID-19 virus spread across India over the last several days.
https://app.powerbi.com/view?r=eyJrIjoiMWE4NGQwYmItZjJlZC00NmE4LWE3M2UtMjYyYzc5ZGJkMTkxIiwidCI6ImY2YjZkZDViLWYwMmYtNDQxYS05OWEwLTE2MmFjNTA2MGJkMiIsImMiOjZ9

This is a data visualization showing the severity of COVID-19 virus by districts in India (indicated with green, orange, and red zones. These are ranked by severity with red being the worst).

https://app.powerbi.com/view?r=eyJrIjoiODNmMGQ5M2YtODcxYS00YTc4LTg0OGMtMDg1YTEzYWIzOGFiIiwidCI6ImY2YjZkZDViLWYwMmYtNDQxYS05OWEwLTE2MmFjNTA2MGJkMiIsImMiOjZ9

### Machine Learning

Inside there are several folders. additional_data, Varun_Alex_Merged_Content, and Varun_Preprocessed_Data1 all contain code that clean our data as the results of feature engineering. We merged the various data sets based on the date and location. The folder machine learning contains three files that each contain four different models. The models in all three are a Support Vector Regression model, a Linear Regression model, a Lasso Regression model, and an Elastic Net Regression model. In all models, we scaled the data and selected the k-best (40) features that resulted in the highest accuracy. Our final model that has the highest accuracy is the Lasso model in each scenario. When predicting how many Positive cases a state has, the model has an accuracy score of 80%. When predicting how many active cases a district has, the model has an accuracy score of 44%. The model that predicts the number of days is not accurate and we would like it to not be considered. All of these accuracies are average of the cross validations with 20 folds.
