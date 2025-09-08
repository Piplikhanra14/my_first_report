import streamlit as st #streamlit import
import pandas as pd #For any chart
import numpy as np #When using random values

st.title("📊 Interactive chart") #title

# ---- choose row number from slider ----
rows = st.slider("How much data you want ?", 5, 100, 20)  # (min=5, max=100, default=20)

# ---- Making data ----
data = pd.DataFrame(
    np.random.randn(rows, 3),   # rows from  slider
    columns=['A', 'B', 'C']
)

st.write(f"Total {rows} row is showing") 
st.line_chart(data)   # line chart