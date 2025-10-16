import streamlit as st
import pandas as pd

# ---------------- GPA Calculation (CUI Grading) ----------------
def get_grade_info(percentage):
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


def calculate_gpa(marks, total_marks, credits):
    total_points = 0
    total_credits = 0
    details = []

    for i, (mark, total, credit) in enumerate(zip(marks, total_marks, credits)):
        percentage = (mark / total) * 100
        grade, grade_point = get_grade_info(percentage)
        total_points += grade_point * credit
        total_credits += credit
        details.append({
            "Subject": f"Subject {i+1}",
            "Marks": f"{mark}/{total}",
            "Percentage": f"{percentage:.2f}%",
            "Grade": grade,
            "Grade Point": grade_point,
            "Credit Hours": credit
        })

    gpa = round(total_points / total_credits, 2) if total_credits else 0
    return gpa, pd.DataFrame(details)


def calculate_cgpa(gpas, credits_list):
    total_points = sum(g * c for g, c in zip(gpas, credits_list))
    total_credits = sum(credits_list)
    return round(total_points / total_credits, 2) if total_credits else 0


# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="CUI GPA & CGPA Calculator", layout="wide")

st.markdown("""
<style>
    .main-title {
        font-size: 40px;
        font-weight: 700;
        text-align: center;
        color: #003366;
        margin-bottom: 10px;
    }
    .sub-title {
        text-align: center;
        color: gray;
        font-size: 18px;
        margin-bottom: 30px;
    }
    .result-box {
        background-color: #f0f8ff;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
        font-size: 22px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎓 CUI GPA & CGPA Calculator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Calculate your GPA & CGPA according to COMSATS grading criteria</div>', unsafe_allow_html=True)

option = st.radio("Select Mode:", ["Calculate GPA", "Calculate CGPA"], horizontal=True)

# ---------------- GPA Section ----------------
if option == "Calculate GPA":
    st.subheader("📘 GPA Calculator")
    num_subjects = st.number_input("Enter number of subjects:", min_value=1, step=1)

    marks, total_marks, credits = [], [], []

    for i in range(int(num_subjects)):
        st.markdown(f"**Subject {i+1}**")
        col1, col2, col3 = st.columns(3)
        with col1:
            marks.append(st.number_input(f"Marks Obtained", min_value=0, step=1, key=f"marks_{i}"))
        with col2:
            total_marks.append(st.number_input(f"Total Marks", min_value=1, value=100, step=1, key=f"total_{i}"))
        with col3:
            credits.append(st.number_input(f"Credit Hours", min_value=1, step=1, key=f"credit_{i}"))
        st.markdown("---")

    if st.button("Calculate GPA", use_container_width=True):
        gpa, df = calculate_gpa(marks, total_marks, credits)
        st.success("✅ GPA calculated successfully!")
        st.dataframe(df, use_container_width=True)
        st.markdown(f'<div class="result-box">📊 Your Semester GPA: {gpa}</div>', unsafe_allow_html=True)

# ---------------- CGPA Section ----------------
else:
    st.subheader("🏫 CGPA Calculator")
    num_semesters = st.number_input("Enter number of semesters:", min_value=1, step=1)

    gpas, sem_credits = [], []
    for i in range(int(num_semesters)):
        st.markdown(f"**Semester {i+1}**")
        col1, col2 = st.columns(2)
        with col1:
            gpas.append(st.number_input(f"GPA", min_value=0.0, max_value=4.0, step=0.01, key=f"gpa_{i}"))
        with col2:
            sem_credits.append(st.number_input(f"Total Credit Hours", min_value=1, step=1, key=f"credits_{i}"))
        st.markdown("---")

    if st.button("Calculate CGPA", use_container_width=True):
        cgpa = calculate_cgpa(gpas, sem_credits)
        st.success("✅ CGPA calculated successfully!")
        st.markdown(f'<div class="result-box">🎯 Your CGPA: {cgpa}</div>', unsafe_allow_html=True)
