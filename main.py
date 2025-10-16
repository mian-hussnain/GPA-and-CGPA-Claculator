# gpa_cgpa_app.py

import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="CUI GPA & CGPA Calculator", layout="wide")
st.markdown(
    """
    <style>
    body {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .stApp {
        background-color: #0E1117;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    div[data-testid="stMetricValue"] {
        font-size: 28px;
        color: #4CAF50;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- HEADER ----------------
st.title("🎓 CUI GPA & CGPA Calculator")
st.markdown("This app calculates **semester GPA** and **overall CGPA** based on the official CUI grading policy (HEC adopted).")

# ---------------- GRADE MAPPING ----------------
def get_grade_point(percentage):
    """Return grade and grade point based on CUI grading policy."""
    if percentage >= 85:
        return "A", 4.00
    elif percentage >= 80:
        return "A-", 3.66
    elif percentage >= 75:
        return "B+", 3.33
    elif percentage >= 71:
        return "B", 3.00
    elif percentage >= 68:
        return "B-", 2.66
    elif percentage >= 64:
        return "C+", 2.33
    elif percentage >= 61:
        return "C", 2.00
    elif percentage >= 58:
        return "C-", 1.66
    elif percentage >= 54:
        return "D+", 1.30
    elif percentage >= 50:
        return "D", 1.00
    else:
        return "F", 0.00

# ---------------- MAIN LOGIC ----------------
st.subheader("📘 Enter Academic Details")

current_sem = st.number_input("Enter your current semester (1–8):", min_value=1, max_value=8, step=1)

all_sem_data = []

# Loop for each semester up to the one entered
for sem in range(1, current_sem + 1):
    st.markdown(f"### 🧾 Semester {sem} Details")

    num_subjects = st.number_input(
        f"Number of subjects in Semester {sem}:",
        min_value=1, step=1, key=f"subs_{sem}"
    )

    subjects = []
    total_grade_points = 0
    total_credits = 0

    for sub in range(1, num_subjects + 1):
        st.markdown(f"**Subject {sub}**")
        marks_obtained = st.number_input(f"Marks obtained (Subject {sub})", min_value=0.0, max_value=100.0, key=f"m_{sem}_{sub}")
        total_marks = st.number_input(f"Total marks (Subject {sub})", min_value=1.0, key=f"t_{sem}_{sub}")
        credit_hours = st.number_input(f"Credit hours (Subject {sub})", min_value=1.0, key=f"c_{sem}_{sub}")
        
        percentage = (marks_obtained / total_marks) * 100
        grade, grade_point = get_grade_point(percentage)
        
        subjects.append({
            "Subject": f"Subject {sub}",
            "Marks": f"{marks_obtained:.0f}/{int(total_marks)}",
            "Percentage": f"{percentage:.2f}%",
            "Grade": grade,
            "Grade Point": grade_point,
            "Credit Hours": credit_hours
        })
        
        total_grade_points += grade_point * credit_hours
        total_credits += credit_hours

    df = pd.DataFrame(subjects)
    st.dataframe(df, use_container_width=True)

    if total_credits > 0:
        sem_gpa = total_grade_points / total_credits
        st.success(f"🎯 Semester {sem} GPA: **{sem_gpa:.2f}**")
        all_sem_data.append((sem_gpa, total_credits))
    else:
        st.warning("Please enter valid credit hours to calculate GPA.")

# ---------------- CALCULATE CGPA ----------------
if st.button("Calculate Overall CGPA"):
    if all_sem_data:
        total_weighted_points = sum([gpa * ch for gpa, ch in all_sem_data])
        total_credit_hours = sum([ch for _, ch in all_sem_data])
        cgpa = total_weighted_points / total_credit_hours
        st.markdown("---")
        st.metric(label=f"🌟 Overall CGPA after Semester {current_sem}", value=f"{cgpa:.2f}")
    else:
        st.error("Please calculate GPA for at least one semester first.")
