import streamlit as st #streamlit import

st.title("About Age") # heading

age = st.slider("What is your age?", 1, 100, 18)   # (min=1, max=100, default=18) by this we can adjust our age

st.write("Your age:  ", age) #in slider which you select that age will appear
