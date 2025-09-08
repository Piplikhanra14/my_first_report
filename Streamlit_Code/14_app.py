import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ------------------ Page Config ------------------
st.set_page_config(
    page_title="Best College Finder",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Best College Finder")
st.write("Upload your college dataset and enter your 6 semester marks to find your best college match.")

# ------------------ Sidebar ------------------
st.sidebar.header("Upload College Data")
uploaded_file = st.sidebar.file_uploader("Upload Excel file", type=["xlsx", "xls"])

# if uploaded file, read data
if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.sidebar.header("Enter Your Semester Marks")
    sem1 = st.sidebar.number_input("Semester 1", 0, 100)
    sem2 = st.sidebar.number_input("Semester 2", 0, 100)
    sem3 = st.sidebar.number_input("Semester 3", 0, 100)
    sem4 = st.sidebar.number_input("Semester 4", 0, 100)
    sem5 = st.sidebar.number_input("Semester 5", 0, 100)
    sem6 = st.sidebar.number_input("Semester 6", 0, 100)

    user_scores = [sem1, sem2, sem3, sem4, sem5, sem6]

    # ------------------ Matching Logic ------------------
    def rank_colleges(user_scores, df):
        df['Diff'] = df.apply(
            lambda row: sum(abs(u - c) for u, c in zip(
                user_scores,
                [row['Avg_Sem1'], row['Avg_Sem2'], row['Avg_Sem3'], 
                 row['Avg_Sem4'], row['Avg_Sem5'], row['Avg_Sem6']]
            )),
            axis=1
        )
        df_sorted = df.sort_values('Diff')
        return df_sorted

    # Button in slidebar to find best colleges
    if st.sidebar.button("Find Best Colleges"):
        ranked = rank_colleges(user_scores, df)

        # Best College Display
        top1 = ranked.iloc[0]['College']
        st.success(f"🏆 Your best college match: **{top1}**")

        # Top 3 College Table
        st.subheader("🏫 Top 3 College Suggestions")
        st.table(ranked[['College', 'Diff']].head(3).reset_index(drop=True))

        # ------------------ Comparison Chart ------------------
        best_row = ranked.iloc[0]
        college_scores = [
            best_row['Avg_Sem1'], best_row['Avg_Sem2'], best_row['Avg_Sem3'],
            best_row['Avg_Sem4'], best_row['Avg_Sem5'], best_row['Avg_Sem6']
        ]

        plt.figure(figsize=(8, 4))
        plt.plot(range(1, 7), user_scores, marker='o', label='Your Scores')
        plt.plot(range(1, 7), college_scores, marker='x', label=f"{top1} Scores")
        plt.xlabel("Semester")
        plt.ylabel("Marks")
        plt.title(f"Your vs {top1} Scores")
        plt.xticks(range(1, 7))
        plt.legend()
        st.pyplot(plt)

else:
    st.info("⬆️ Please upload your college dataset in Excel format to proceed.")