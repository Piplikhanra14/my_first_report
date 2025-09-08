import streamlit as st #streamlit import
import pandas as pd #For any chart
import numpy as np #When using random values

st.title("Chart Example")

# We are making data frame with random values
data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['A', 'B', 'C']
)

st.line_chart(data)   # shows line chart
st.bar_chart(data)    # shows bar chart
st.area_chart(data)   # shows area chart
st.table(data)        # shows data in table format
st.dataframe(data)    # shows data in dataframe format
st.json({
    'name': 'Streamlit',
    'type': 'Library',
    'language': 'Python'
})  # shows data in json format
st.metric(label="Temperature", value="70 °F", delta="1.2 °F")  # shows metric
st.metric(label="Humidity", value="80 %", delta="-5 %")  # shows metric
