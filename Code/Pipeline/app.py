import streamlit as st
import time
from predict import show_predict_page
from explore_page_2 import show_explore_page
import os
import pickle
from airbnb_ETL import DataInterface
import re
#from airbnb_insights import RecommendationEngine 
#from airbnb_insights import Insight
from stats import show_statistics


st.set_page_config(page_title='AirBnB')


city_re = re.compile('DataInterface_(.*)\.obj')
city_list = [city_re.findall(file)[0] for file in os.listdir('.') if city_re.match(file)]

with st.spinner('Loading...'):
    time.sleep(0.1)


city=st.sidebar.selectbox('Select City :',city_list)



@st.cache
def get_data_interface(city):
    return pickle.load(open(f'DataInterface_{city}.obj','rb'))

data_interface=get_data_interface(city)


def get_revenue_model():
    return data_interface.get_model('revenue')

def get_booking_rate_model():
    return data_interface.get_model('booking_rate')



model_seattle_revenue = get_revenue_model()



model_seattle_booking_rate = get_booking_rate_model()



def get_data():
    return data_interface.get_data()[1]


def get_insight_engine():
    return data_interface.get_recommendation_engine()

df=get_data()




page = st.sidebar.radio('Explore Data Or Predict', ("Predict", "Explore Data","Statistics"),horizontal =True)

if page == "Predict":
    show_predict_page(city,df,model_seattle_revenue,model_seattle_booking_rate,get_insight_engine().describe)
    
elif page == 'Statistics':
    show_statistics(get_insight_engine().describe)   
else:
    show_explore_page(get_insight_engine().insights)
    



    



