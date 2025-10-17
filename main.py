import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# -----------------------------
# GPA & CGPA Calculation Logic
# -----------------------------
def calculate_gpa(marks, total_marks, credits):
    total_points = 0
    total_credits = 0
    for mark, total, credit in zip(marks, total_marks, credits):
        percentage = (mark / total) * 100
        # GPA scale
        if percentage >= 90:
            grade_point = 4.0
        elif percentage >= 85:
            grade_point = 3.7
        elif percentage >= 80:
            grade_point = 3.3
        elif percentage >= 75:
            grade_point = 3.0
        elif percentage >= 70:
            grade_point = 2.7
        elif percentage >= 65:
            grade_point = 2.3
        elif percentage >= 60:
            grade_point = 2.0
        elif percentage >= 50:
            grade_point = 1.5
        else:
            grade_point = 0.0

        total_points += grade_point * credit
        total_credits += credit

    return round(total_points / total_credits, 2) if total_credits != 0 else 0


def calculate_cgpa(gpas, credits_list):
    total_points = 0
    total_credits = 0
    for gpa, credit in zip(gpas, credits_list):
        total_points += gpa * credit
        total_credits += credit
    return round(total_points / total_credits, 2) if total_credits != 0 else 0


# -----------------------------
# Streamlit App
# -----------------------------
st.set_page_config(page_title="🎓 GPA & CGPA Calculator", layout="wide")

st.title("🎓 GPA & CGPA Calculator")

option = st.selectbox("Choose an option:", ["Calculate GPA & CGPA", "Use Previous GPA Data"])

if option == "Calculate GPA & CGPA":
    num_semesters = st.number_input("Enter number of semesters:", min_value=1, step=1)

    gpas = []
    sem_credits = []

    for i in range(int(num_semesters)):
        st.markdown(f"### 📘 Semester {i+1}")
        num_subjects = st.number_input(f"Enter number of subjects for semester {i+1}:", min_value=1, step=1, key=f"sub_{i}")

        marks, total_marks, credits = [], [], []
        for j in range(int(num_subjects)):
            st.write(f"**Subject {j+1}**")
            marks.append(st.number_input(f"Marks obtained (Subject {j+1})", min_value=0.0, step=1.0, key=f"mark_{i}_{j}"))
            total_marks.append(st.number_input(f"Total marks (Subject {j+1})", min_value=1.0, value=100.0, step=1.0, key=f"total_{i}_{j}"))  # ✅ Default 100
            credits.append(st.number_input(f"Credit hours (Subject {j+1})", min_value=1.0, step=1.0, key=f"credit_{i}_{j}"))

        gpa = calculate_gpa(marks, total_marks, credits)
        total_credit = sum(credits)
        gpas.append(gpa)
        sem_credits.append(total_credit)

        st.success(f"GPA for Semester {i+1}: {gpa}")

    if st.button("Calculate CGPA"):
        cgpa = calculate_cgpa(gpas, sem_credits)
        st.markdown("---")
        st.success(f"🏆 Your overall CGPA is: **{cgpa}**")

        # Optional GPA Trend Graph
        semesters = [f"Sem {i+1}" for i in range(len(gpas))]
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=semesters, y=gpas, mode='lines+markers',
            line=dict(color='royalblue', width=3), marker=dict(size=10)
        ))
        fig.update_layout(title="GPA Trend Over Semesters", xaxis_title="Semester", yaxis_title="GPA", height=400)
        st.plotly_chart(fig, use_container_width=True)

elif option == "Use Previous GPA Data":
    num_semesters = st.number_input("Enter number of previous semesters:", min_value=1, step=1)

    gpas = []
    sem_credits = []

    for i in range(int(num_semesters)):
        gpas.append(st.number_input(f"GPA for semester {i+1}:", min_value=0.0, max_value=4.0, step=0.01, key=f"gpa_{i}"))
        sem_credits.append(st.number_input(f"Total credit hours for semester {i+1}:", min_value=1.0, step=1.0, key=f"cred_{i}"))

    if st.button("Calculate CGPA"):
        cgpa = calculate_cgpa(gpas, sem_credits)
        st.success(f"🏆 Your overall CGPA is: **{cgpa}**")
