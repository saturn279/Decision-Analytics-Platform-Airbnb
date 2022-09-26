import warnings
import streamlit as st
from airbnb_ETL import DataInterface

warnings.filterwarnings("ignore")
import pandas as pd
calendar_df=pd.read_csv('http://data.insideairbnb.com/united-states/wa/seattle/2022-06-15/data/calendar.csv.gz')
listings_link='http://data.insideairbnb.com/united-states/wa/seattle/2022-06-15/data/listings.csv.gz'
listings_df = pd.read_csv(listings_link)
# Extract money value

def extract_value(text):
    if isinstance(text, str):
        text = text.replace('$','')
        text = text.replace(',','')
        text = text.replace('%','')
        value = float(text.replace('$',''))
    else:
        value=text
    return value


def cleaning_df(cleaned_df):
  mylist=cleaned_df[cleaned_df.columns[cleaned_df.isnull().any()]].isnull().columns
  dtype_num=cleaned_df[mylist].select_dtypes(include=['float64','int64']).columns
  for col in dtype_num:
    cleaned_df[col]=cleaned_df[col].fillna(cleaned_df[col].mean())
  cleaned_df['host_location']=cleaned_df['host_location'].fillna('host location not available')
  cleaned_df['host_response_time']=cleaned_df['host_response_time'].fillna('response not available')
  cleaned_df['host_is_superhost']=cleaned_df['host_is_superhost'].fillna(cleaned_df['host_is_superhost'].mode()[0])
  cleaned_df['host_neighbourhood']=cleaned_df['host_neighbourhood'].fillna('host neighbourhood not available')
  cleaned_df['neighbourhood']=cleaned_df['neighbourhood'].fillna('neighbourhood not available')
  cleaned_df['bathrooms_text']=cleaned_df['bathrooms_text'].fillna(cleaned_df['bathrooms_text'].mode()[0])  
  return cleaned_df


def get_processed_dfs(calendar_df, listings_df):
        listings_df['price'] = listings_df['price'].apply(lambda x: extract_value(x))
        calendar_df['price'] = calendar_df['price'].apply(lambda x: extract_value(x))
        calendar_df['available'] = calendar_df['available'].map({'t':1, 'f':0})
        calendar_df['revenue'] = calendar_df['price']*calendar_df['available']
        
        calendar_df = calendar_df.fillna(0)
        overview = calendar_df.groupby('listing_id').mean()
        overview['daily_revenue'] = overview['revenue']
        overview['booking_rate(%)'] = overview['available']*100
        calendar_booked = calendar_df[calendar_df['price']!=0]
        calendar_booked = calendar_booked.groupby('listing_id').agg({'price':['mean','std']}).reset_index()
        calendar_booked.columns=['listing_id','price_avg','price_std']
        pricing_strategies = ['price', 'accommodates']

        for col in pricing_strategies:
                  listings_df[col] = listings_df[col].apply(lambda x: extract_value(x))
        listings_df = listings_df.drop('price', axis=1)
        overview = overview[['available', 'price', 'revenue',
                  'daily_revenue', 'booking_rate(%)']]
        listings_df = pd.merge(listings_df, overview, how='left', left_on='id', right_on='listing_id')
        listings_df = pd.merge(listings_df, calendar_booked, how='left', left_on='id', right_on='listing_id')
        listings_df['price_per_person'] = listings_df['price'] / listings_df['accommodates']
        listings_df = listings_df.drop(['listing_id'], axis=1)
        listings_df['accom_per_bed'] = listings_df['accommodates']/listings_df['beds']
        listings_df['price_surge_percent'] = (listings_df['price_avg']/listings_df['price']-1)*100
        
        #To check abrupt changes in price during peak season
        listings_df['price_std_percent'] = listings_df['price_std']/listings_df['price']*100
        columns=['host_location','host_response_time','host_response_rate','host_acceptance_rate','host_is_superhost','host_neighbourhood','host_total_listings_count','host_verifications',
        'host_identity_verified','neighbourhood','property_type','room_type','bedrooms','minimum_nights','maximum_nights','has_availability','availability_30','number_of_reviews','number_of_reviews_ltm',
        'number_of_reviews_l30d','review_scores_rating','review_scores_accuracy','review_scores_cleanliness','review_scores_checkin','review_scores_communication','review_scores_location','review_scores_value',
        'instant_bookable','price','price_avg','price_std','beds','accommodates','reviews_per_month','availability_60','availability_90','availability_365','revenue','booking_rate(%)','bathrooms_text','price_per_person',
        'accom_per_bed','price_surge_percent','price_std_percent']
        cleaned_df=listings_df[columns]
        cleaned_df['host_response_rate'] = cleaned_df['host_response_rate'].apply(lambda x: extract_value(x))
        cleaned_df['host_acceptance_rate'] = cleaned_df['host_acceptance_rate'].apply(lambda x: extract_value(x))
        cleaned_df=cleaning_df(cleaned_df)
        return cleaned_df
insights_df=get_processed_dfs(calendar_df, listings_df)

insights_df.isnull().sum()
features=['price', 'price_avg', 'price_per_person', 'availability_365', 'beds',
        'accommodates', 'availability_60', 'review_scores_rating',
        'reviews_per_month', 'availability_30','revenue','booking_rate(%)']
df=insights_df[features]

X_revenue=df.drop(['revenue','price_per_person','price_avg','booking_rate(%)'],axis=1)
y_revenue=df.revenue

X_rate=df.drop(['revenue','price_per_person','price_avg','booking_rate(%)'],axis=1)
y_rate=df['booking_rate(%)']


# =============================================================================
# from xgboost import XGBRegressor
# from sklearn.model_selection import GridSearchCV
# from sklearn.model_selection import KFold
# 
# import pickle
# 
# #
# model_xgb=XGBRegressor(random_state=2022)
# kfold=KFold(n_splits=5,shuffle=True,random_state=2022)
# params={'max_depth':[2,3,4,5,6],'n_estimators':[50,100],'learning_rate':[0.01,0.3,0.05,0.5,0.7]}
# gcv_xgb=GridSearchCV(model_xgb,scoring='r2',param_grid=params,cv=kfold,verbose=3)
# gcv_xgb.fit(X_revenue,y_revenue)
# model_revenue=gcv_xgb.best_estimator_
# print('Best score  : ',gcv_xgb.best_score_)
# print('Best params  : ',gcv_xgb.best_params_)
# #
# model_xgb=XGBRegressor(random_state=2022)
# kfold=KFold(n_splits=5,shuffle=True,random_state=2022)
# params={'max_depth':[2,3,4,5,6],'n_estimators':[50,100],'learning_rate':[0.01,0.3,0.05,0.5,0.7]}
# gcv_xgb=GridSearchCV(model_xgb,scoring='r2',param_grid=params,cv=kfold,verbose=3)
# gcv_xgb.fit(X_rate,y_rate)
# model_b=gcv_xgb.best_estimator_
# print('Best score  : ',gcv_xgb.best_score_)
# print('Best params  : ',gcv_xgb.best_params_)
# 
# pickle.dump(model_b,open('D:\Project\Streamlit\model_booking_rate.pkl','wb'))
# pickle.dump(model_revenue,open('D:\Project\Streamlit\model_xgb.pkl','wb'))
# =============================================================================

def insights():
    return insights_df

def features():
    return df