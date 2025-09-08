import streamlit as st #streamlit import
import pandas as pd #For any chart

st.title("My Marks Chart") #title

data = pd.DataFrame({
    "Subject": ["Math", "English", "Science"],
    "Marks": [80, 65, 90]
}) #Input differnt values

st.bar_chart(data.set_index("Subject")) # Bar chart
