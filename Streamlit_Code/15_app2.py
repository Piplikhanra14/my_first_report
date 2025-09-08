# advanced_app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

# ---------------- Page config ----------------
st.set_page_config(page_title="Best College Finder (Advanced)",
                   page_icon="🎓", layout="wide")

st.title("🎓 Best College Finder — Advanced")
st.write("Upload a college dataset (Excel/CSV) or download the sample, enter your 6 semester marks, "
         "adjust weights/normalization, then press **Find Best Colleges**.")

# ---------------- Sample dataset download ----------------
def make_sample_excel_bytes():
    sample = pd.DataFrame([
        {"College":"College A","Avg_Sem1":70,"Avg_Sem2":72,"Avg_Sem3":68,"Avg_Sem4":75,"Avg_Sem5":78,"Avg_Sem6":80},
        {"College":"College B","Avg_Sem1":65,"Avg_Sem2":70,"Avg_Sem3":72,"Avg_Sem4":74,"Avg_Sem5":76,"Avg_Sem6":77},
        {"College":"College C","Avg_Sem1":80,"Avg_Sem2":82,"Avg_Sem3":79,"Avg_Sem4":81,"Avg_Sem5":83,"Avg_Sem6":85},
        {"College":"College D","Avg_Sem1":55,"Avg_Sem2":58,"Avg_Sem3":60,"Avg_Sem4":62,"Avg_Sem5":65,"Avg_Sem6":68},
    ])
    towrite = BytesIO()
    with pd.ExcelWriter(towrite, engine="openpyxl") as writer:
        sample.to_excel(writer, index=False, sheet_name="Sheet1")
    towrite.seek(0)
    return towrite.getvalue()

st.sidebar.download_button("🔽 Download sample dataset (xlsx)", make_sample_excel_bytes(),
                           file_name="college_sample.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# ---------------- File uploader ----------------
st.sidebar.header("1) Upload college dataset")
uploaded_file = st.sidebar.file_uploader("Upload Excel (.xlsx/.xls) or CSV (.csv)", type=["xlsx","xls","csv"])

# ---------------- Utility: flexible column finder ----------------
def normalize_colname(s):
    return ''.join(ch.lower() for ch in str(s) if ch.isalnum())

def find_column_by_candidates(df_cols, candidates):
    norm_map = {normalize_colname(c): c for c in df_cols}
    # direct match
    for cand in candidates:
        if cand in norm_map:
            return norm_map[cand]
    # contains match
    for k,orig in norm_map.items():
        for cand in candidates:
            if cand in k:
                return orig
    return None

# ---------------- If file uploaded -> process ----------------
if uploaded_file:
    # read
    try:
        if uploaded_file.name.lower().endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.sidebar.error(f"Failed to read file: {e}")
        st.stop()

    st.sidebar.success(f"Loaded `{uploaded_file.name}` — {df.shape[0]} rows, {df.shape[1]} cols")
    st.write("**Preview of uploaded data:**")
    st.dataframe(df.head(5))

    # try to detect required columns
    cols = list(df.columns)
    college_col = find_column_by_candidates(cols, ["college","name","collegename","institution","institute"])
    sem_cols = []
    for i in range(1,7):
        candidates = [f"avgsem{i}", f"sem{i}", f"semester{i}", f"avgsemester{i}", f"sem{i}avg"]
        col = find_column_by_candidates(cols, candidates)
        sem_cols.append(col)

    # validation
    missing = []
    if college_col is None:
        missing.append("College column (try name 'College')")
    for i, c in enumerate(sem_cols, start=1):
        if c is None:
            missing.append(f"Avg_Sem{i} column (try 'Avg_Sem{i}' or 'Sem{i}')")

    if missing:
        st.error("Column name problem — please ensure your file has these columns:\n\n- " + "\n- ".join(missing))
        st.info("Detected columns: " + ", ".join(cols))
        st.stop()

    # reorder dataframe to a consistent structure
    proc = df[[college_col] + sem_cols].copy()
    proc.columns = ["College"] + [f"Avg_Sem{i}" for i in range(1,7)]

    # ---------------- Sidebar: user marks & options ----------------
    st.sidebar.header("2) Enter your semester marks")
    sem1 = st.sidebar.number_input("Semester 1", 0.0, 100.0, 70.0, step=1.0, format="%.2f")
    sem2 = st.sidebar.number_input("Semester 2", 0.0, 100.0, 72.0, step=1.0, format="%.2f")
    sem3 = st.sidebar.number_input("Semester 3", 0.0, 100.0, 68.0, step=1.0, format="%.2f")
    sem4 = st.sidebar.number_input("Semester 4", 0.0, 100.0, 75.0, step=1.0, format="%.2f")
    sem5 = st.sidebar.number_input("Semester 5", 0.0, 100.0, 78.0, step=1.0, format="%.2f")
    sem6 = st.sidebar.number_input("Semester 6", 0.0, 100.0, 80.0, step=1.0, format="%.2f")
    user_scores = np.array([sem1, sem2, sem3, sem4, sem5, sem6], dtype=float)

    st.sidebar.header("3) Options")
    normalize = st.sidebar.checkbox("Normalize college scores (min-max → 0-100) before comparison", value=False)
    metric = st.sidebar.selectbox("Distance metric", ["Absolute (L1)", "Euclidean (L2)"])
    st.sidebar.markdown("**Weights for semesters** (importance). They will be normalized to sum=1.")
    use_equal_weights = st.sidebar.checkbox("Use equal weights", value=True)
    if use_equal_weights:
        weights = np.ones(6, dtype=float)
    else:
        weights = np.array([
            st.sidebar.slider(f"W{i}", 0.0, 2.0, 1.0, step=0.01) for i in range(1,7)
        ], dtype=float)
    # normalize weights to sum 1 (avoid zero-sum)
    if weights.sum() <= 0:
        weights = np.ones(6, dtype=float)
    weights = weights / weights.sum()

    top_n = st.sidebar.slider("How many top colleges to show", 1, min(20, max(3, proc.shape[0])), 3)

    # ---------------- Preprocess (optional normalization) ----------------
    proc2 = proc.copy()
    mins = proc2[[f"Avg_Sem{i}" for i in range(1,7)]].min()
    maxs = proc2[[f"Avg_Sem{i}" for i in range(1,7)]].max()

    if normalize:
        for i in range(1,7):
            col = f"Avg_Sem{i}"
            if maxs[col] > mins[col]:
                proc2[col] = (proc2[col] - mins[col]) / (maxs[col] - mins[col]) * 100
            else:
                proc2[col] = 50.0  # constant column -> set neutral 50

        # normalize user scores using same mins/maxs
        user_norm = user_scores.copy()
        for i in range(6):
            col = f"Avg_Sem{i+1}"
            if maxs[col] > mins[col]:
                user_norm[i] = (user_scores[i] - mins[col]) / (maxs[col] - mins[col]) * 100
            else:
                user_norm[i] = 50.0
        user_scores_used = user_norm
    else:
        user_scores_used = user_scores.copy()

    # ---------------- Compute distances (vectorized) ----------------
    vals = proc2[[f"Avg_Sem{i}" for i in range(1,7)]].values.astype(float)  # (n_rows, 6)
    user_row = user_scores_used.reshape(1,6)  # (1,6)

    if metric == "Absolute (L1)":
        diffs = np.sum(np.abs(vals - user_row) * weights.reshape(1,6), axis=1)
    else:  # Euclidean: sqrt(sum(weights * diff^2))
        diffs = np.sqrt(np.sum(weights.reshape(1,6) * (vals - user_row)**2, axis=1))

    proc2["Diff"] = diffs
    ranked = proc2.sort_values("Diff").reset_index(drop=True)
    ranked["Rank"] = ranked.index + 1

    # ---------------- Show results when user clicks button ----------------
    if st.sidebar.button("Find Best Colleges"):
        st.success(f"🏆 Best match: **{ranked.loc[0,'College']}**  (Diff = {ranked.loc[0,'Diff']:.2f})")

        # Top-N table
        st.subheader(f"Top {top_n} college suggestions")
        st.table(ranked[["Rank","College","Diff"]].head(top_n))

        # Metrics cards (user avg vs top1 avg)
        col1, col2, col3 = st.columns(3)
        user_avg = float(np.mean(user_scores_used))
        top1_vals = ranked.loc[0, [f"Avg_Sem{i}" for i in range(1,7)]].values.astype(float)
        top1_avg = float(np.mean(top1_vals))
        col1.metric("Your average (used)", f"{user_avg:.2f}")
        col2.metric(f"{ranked.loc[0,'College']} average", f"{top1_avg:.2f}")
        col3.metric("Difference (avg)", f"{(user_avg - top1_avg):+.2f}")

        # Comparison line chart (user vs best)
        plt.figure(figsize=(8,4))
        plt.plot(range(1,7), user_scores_used, marker='o', label='Your (used)')
        plt.plot(range(1,7), top1_vals, marker='x', label=f"{ranked.loc[0,'College']}")
        plt.xlabel("Semester")
        plt.ylabel("Marks")
        plt.title("Your vs Best College (by semester)")
        plt.xticks(range(1,7))
        plt.legend()
        st.pyplot(plt)

        # Bar chart of top_n diffs
        plt.figure(figsize=(8,3))
        topn = ranked.head(top_n)
        plt.barh(topn["College"][::-1], topn["Diff"][::-1])
        plt.xlabel("Distance (lower is better)")
        plt.title(f"Top {top_n} — Distance")
        st.pyplot(plt)

        # Download ranked results CSV
        csv_bytes = ranked.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download full ranked results (CSV)", data=csv_bytes,
                           file_name="ranked_colleges.csv", mime="text/csv")

else:
    st.info("Upload a college dataset (or download the sample) to begin.")

