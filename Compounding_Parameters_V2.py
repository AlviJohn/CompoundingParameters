# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 09:33:42 2022

@author: alvi
"""
import streamlit as st
import numpy as np
import pandas as pd
from chart_studio import plotly as py
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from itertools import product
from datetime import datetime
from PIL import Image



#######Setting the Basics for the Page
st.set_page_config(page_title="Compounding_Parameters", page_icon="muscleman.jpg", layout="wide", initial_sidebar_state="auto")
st.title('Compounding Parameters')
Compound_parameter_dataset = pd.read_csv('LIMS_analytical_dataset_V5.csv',encoding="cp1252") 



component_variable = st.selectbox(
     'Please Select the Component',Compound_parameter_dataset['ComponentName'].unique().tolist())

Compound_parameter_dataset=Compound_parameter_dataset.loc[
        (Compound_parameter_dataset['ComponentName'] == component_variable),:]


compound_variable = st.selectbox(
     'Please Select the Compound',Compound_parameter_dataset['Material'].unique().tolist())

Compound_parameter_dataset=Compound_parameter_dataset.loc[
        (Compound_parameter_dataset['Material']==compound_variable),:]



################################################################################################################
#compoundcode_variable = st.selectbox(
#     'Please Select the Compound Code',Compound_parameter_dataset['BanburyMaterialCode'].unique().tolist())

#Compound_parameter_dataset=Compound_parameter_dataset.loc[
#        (Compound_parameter_dataset['BanburyMaterialCode']==compoundcode_variable),:]

############################################################################################################

Variables = [
'PMDRMH_Actual',
'PMDRT90_Actual',
'PMIV_Actual',
'PMV_Actual',
'PT35_Actual',
'PT5_Actual',
'PSPGR_Actual'
]

option = st.selectbox(
     'Please Select the Variable',Variables)


Compound_parameter_dataset=Compound_parameter_dataset.loc[
        (Compound_parameter_dataset[option] > 0),:]

###################################################################################
metric_option = st.selectbox('Select the Metric',['RFPP Only', 'Imbalance only','Imbalance & RFPP'])
if metric_option=='RFPP Only':
    var1='Rejection_RFPP_Only'
elif metric_option=='Imbalance only':
    var1='Rejection_Imbalance_Only'
elif metric_option=='Imbalance & RFPP':
    var1='Rejection_RFPP_Imbalance'
#################################################################################


Compound_parameter_dataset_1sttest = Compound_parameter_dataset.loc[Compound_parameter_dataset['timeperiod'].isin(['Test 1','Control 1']),:]
Compound_parameter_dataset_2ndtest = Compound_parameter_dataset.loc[Compound_parameter_dataset['timeperiod'].isin([ 'Test 2','Control 2']),:]

#Compound_parameter_dataset_2ndtest =Compound_parameter_dataset
##########Charts#########################
var = option
upper = option.replace("_Actual", "_Upper_Spec")
lower=option.replace("_Actual", "_Lower_Spec")


temp1_minmax= Compound_parameter_dataset_1sttest.groupby(['gt_date','timeperiod']).\
                    agg({upper:'max', lower:'min'}).\
                    reset_index()
                    
temp2_minmax=Compound_parameter_dataset_2ndtest.groupby(['gt_date','timeperiod']).\
                    agg({upper:'max', lower:'min'}).\
                    reset_index()

  
#temp2_minmax=Compound_parameter_dataset.groupby(['gt_date','timeperiod']).\
#                    agg({upper:'max', lower:'min'}).\
#                    reset_index()
                    
fig = px.box(Compound_parameter_dataset_1sttest, y=var, x="gt_date",color='BanburyMaterialCode')
fig.update_layout(title_text= str(var) + " VS Rejection Time Series(Test-30Mar to 3Apr,Control-25Mar to 29Mar(5days)")
fig.add_scatter(x=temp1_minmax['gt_date'], y=temp1_minmax[lower],mode ='markers',name='lower spec')
fig.add_scatter(x=temp1_minmax['gt_date'], y=temp1_minmax[upper],mode ='markers',name='upper spec')
st.plotly_chart(fig,use_container_width=True)


#*************************************************************************************************
fig = px.box(Compound_parameter_dataset_2ndtest, y=var, x="gt_date",color='BanburyMaterialCode')
fig.update_layout(title_text= str(var) + " VS Rejection Time Series(Test-24Apr to 1May,Control-17Apr to 23Apr(7days)")
fig.add_scatter(x=temp2_minmax['gt_date'], y=temp2_minmax[lower],mode ='markers',name='lower spec')
fig.add_scatter(x=temp2_minmax['gt_date'], y=temp2_minmax[upper],mode ='markers',name='upper spec')
st.plotly_chart(fig,use_container_width=True)

#st.write(Compound_parameter_dataset_1sttest.groupby(['timeperiod',var1])['BARCODE'].count())
#st.write(Compound_parameter_dataset_2ndtest.groupby(['timeperiod',var1])['BARCODE'].count())



















































#col1, col2 = st.sidebar.columns(2)
#with col1:
#    start_date = st.date_input('Start date', min_date)
#with col2:
#        end_date = st.date_input('End date', max_date)
#        
#if start_date > end_date:
#    st.error('Error: End date must fall after start date.')
#        
#RC_with_DR = RC_with_DR[(RC_with_DR['Createddate'] >= start_date) & (RC_with_DR['Createddate'] <= end_date)]
#
#
#
####Select Rim Sizes
#rim_choices = RC_with_DR['Rim_Size_new'].unique().tolist()
#rim_choices.insert(0,"ALL")
#rim_make_choice = st.sidebar.multiselect("Select one or more Rim Sizes:",rim_choices,'ALL')
#if "ALL" in rim_make_choice:
#    rim_make_choice_final = rim_choices
#else:
#    rim_make_choice_final = rim_make_choice
#
#RC_with_DR=RC_with_DR.loc[(RC_with_DR['Rim_Size_new'].isin(rim_make_choice_final))]
#####First Chart
#RC_with_DR = RC_with_DR.dropna()
#
#
#
####Select Aspect Ratio
#ar_choices = RC_with_DR['aspect_ratio'].unique().tolist()
#ar_choices.insert(0,"ALL")
#ar_make_choice = st.sidebar.multiselect("Select one or more Aspect Ratios:",ar_choices,'ALL')
#if "ALL" in ar_make_choice:
#    ar_make_choice_final = ar_choices
#else:
#    ar_make_choice_final = ar_make_choice
#RC_with_DR=RC_with_DR.loc[(RC_with_DR['aspect_ratio'].isin(ar_make_choice_final))]
#
#
####Select Capcompound
#cap_choices = RC_with_DR['CapCompound'].unique().tolist()
#cap_choices.insert(0,"ALL")
#cap_make_choice = st.sidebar.multiselect("Select one or more Cap Compounds:",cap_choices,'ALL')
#if "ALL" in cap_make_choice:
#    cap_make_choice_final = cap_choices
#else:
#    cap_make_choice_final = cap_make_choice
#
#
#RC_with_DR=RC_with_DR.loc[(RC_with_DR['CapCompound'].isin(cap_make_choice_final))]
#
#####Removing Duplicates
#RC_with_DR = RC_with_DR.dropna()
#st.write("After filtering",RC_with_DR.shape[0], " observations were filtered for the dashboard" )
#
#csv= RC_with_DR.to_csv().encode('utf-8')
#st.download_button(
#   "Click to Download Data",
#    csv,
#   "RRC Data.csv",
#   "text/csv",
#   key='download-csv'
#   )
#
#
#image = Image.open('muscle_man2.png')
#st.sidebar.image(image)
#
#
#
#
########################################################Charts
#####First Chart
#fig = go.Figure()
#
#fig = px.scatter(RC_with_DR, x="Createddate", y="CRR", color='CapCompound')
#st.plotly_chart(fig,use_container_width=True)
#





