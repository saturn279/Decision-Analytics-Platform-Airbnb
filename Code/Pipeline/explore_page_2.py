import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
import re

import pickle
from airbnb_ETL import DataInterface


def show_explore_page(insights):
     index_lst=[]
     i=0
     for insight in insights:
         i+=1
         st.subheader(insight.title,anchor=f'{i}')
         st.pyplot(insight.plot)
         if insight.text is not None:
             st.write("#####",insight.text)
         st.write("-" * 34)
         index_lst.append(f"- [{insight.title}](#{i})")
     st.sidebar.markdown(f'''<h2> Index \n''', unsafe_allow_html=True)
     st.sidebar.markdown('\n\n'.join(index_lst), unsafe_allow_html=True)
     st.sidebar.markdown('</h2>', unsafe_allow_html=True)
     


 