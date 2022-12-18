#!/usr/bin/env python
# coding: utf-8

# In[35]:


import pandas as pd
import streamlit as st
import os
import plotly.express as px
from IPython import get_ipython
import git


# In[57]:


#file_dir = os.listdir (r'C:\Joey 2022')
#file_dir = r'C:\Users\joey0\Downloads'
#file_name = 'df1.csv'
#filepath = f"{file_dir}/{file_name}"

#filepath = 'df1.csv'

#""" App Interface  """
csv_path = "https://raw.githubusercontent.com/joey-van-alphen2/dashboard/main/df1.csv"
    
def main():
	#git clone https://github.com/joey-van-alphen2/verwarming-water-dashboard.git
	os.system("git config --global user.name 'joey-van-alphen2'")
	os.system("git config --global user.email 'joey.van.alphen@hva.nl'")

        
	st.title('Verwarming en Water verbruik')
	df1 = pd.read_csv(csv_path)
    
	st.sidebar.header('Verbruik per datum')
	with st.sidebar.form(key='df1', clear_on_submit=True):
		add_col1 = st.date_input("Datum")
		add_col2 = st.number_input('Verwarming', min_value=0000.00)
		add_col3 = st.number_input('Water', min_value=000.0)
		submit = st.form_submit_button('Submit')
		if submit:
			new_data = {'Datum': add_col1, 'Verwarming': add_col2, 'Water': add_col3}

			df1 = df1.append(new_data, ignore_index=True)
			df1.to_csv('df1.csv', index=False)
        
	os.system("git add df1.csv")
	os.system('git commit -m "Updated CSV file"')
	os.system("git push origin master")


	df1['Datum'] = pd.to_datetime(df1['Datum'], format='%Y-%m-%d')
	df1['GJ'] = df1.Verwarming.diff().fillna(0)
	df1['m3'] = df1.Water.diff().fillna(0)
	fig1 = px.bar(df1, x='Datum', y='GJ', title='Stadsverwarming verbruik in GJ')
	fig2 = px.bar(df1, x='Datum', y='m3', title='Water verbruik in m3')
    
        # create three columns
	kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    # fill in those three columns with respective metrics or KPIs
	kpi1.metric(
		label="Totaal verbruik (GJ) 🔥",
		value=f'{round(df1.GJ.sum(), 2)} GJ')

	kpi2.metric(
		label="Kosten verwarming 💰",
		value=f'€{round((df1.GJ.sum()*47.38), 2)}')

	kpi3.metric(
		label="Totaal verbruik (m3) 💧",
		value= f'{round((df1.m3.sum()), 2)} m3')
    
	kpi4.metric(
		label="Kosten water 💰",
		value=f'€{round((df1.m3.sum()*0.87), 2)}')
    
	st.header('Verbruik afgelopen week')
	st.dataframe(df1.tail(7))
	st.plotly_chart(fig1) 
	st.plotly_chart(fig2)


if __name__ == '__main__':
	main()


# In[55]:


#pd.read_csv(csv_path)

