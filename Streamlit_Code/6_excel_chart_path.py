import streamlit as st #streamlit import
import pandas as pd #For any chart

st.title("📂 Local Excel File Example")

df = pd.read_excel("C:\\Users\\PIPLI KHANRA\Desktop\\Internship\\STUDY MATERIAL\\Cookie Types.xlsx")  # path to your local excel file
st.dataframe(df)
st.bar_chart(df.set_index(df.columns[0]))# df.columns[0] means it takes the first column of the dataframe as index
# if you want to give the name of the index then use   df.set_index("Subject") 
