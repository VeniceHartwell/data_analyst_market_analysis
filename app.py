# Import streamlit and oher necessary libraries for interactive analysis
import streamlit as st
st.title('Career Skillset Analysis')

import pandas as pd # dataframe mgmt
import plotly.express as px # libraries for visualization
import codecs
import streamlit.components.v1 as components

# LOAD csv for skillset analysis
@st.cache
def load_data():
    return pd.read_csv('output/linkedin_skill_requirements_full_2022-09-01.csv')

# IMPORT database
df = load_data()

# OPTION check most popular skills by job
df_options = st.selectbox('Select a job to analyze:', 
    options = ['Data Analyst', 'Data Scientist', 'Data Engineer', 'Data Architect', 'Data Manager'])

# PRINT number of jobs to console
num_jobs = len(df.loc[df['job'] == df_options])

# SELECTED JOB DISPLAYED AS DATAFRAME ordered by top skills
df_filtered = df.loc[df['job'] == f'{df_options}'].groupby('job').mean()*100
df_filtered = df_filtered.T
st.write(f'Total {df_options} jobs: {num_jobs}')
df_ranked = df_filtered.sort_values(by=[f'{df_options}'], ascending=False)
#st.dataframe(df_ranked)

# SELECTED JOB DISPLAYED AS CHART showing only top 30 skills
df_top30 = df_filtered.sort_values(by=[f'{df_options}'], ascending=False).head(30)
x_val = df_options
y_val = df_top30.index
plot = px.bar(df_top30, x=x_val, y=y_val, title=f'Skill Requirements for {df_options}s (by %)', template='plotly')
# FIX: plot.update_layout(labels={"x_val":f"Job: {df_options}", "y_val":"Skills"})
st.plotly_chart(plot, use_container_width=True)

# DATAFRAME visualize skill frequency per job
st.write('## Skills Required by Job (%)',
    round(df.groupby('job').mean()*100, 2))
