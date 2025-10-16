import streamlit as st
import pandas as pd

# ---------------- GPA Logic (CUI Grading) ----------------
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
        font-size: 38px;
        font-weight: 700;
        text-align: center;
        color: #003366;
        margin-bottom: 10px;
    }
    .sub-title {
        text-align: center;
        color: gray;
        font-size: 17px;
        margin-bottom: 25px;
    }
    .result-box {
        background-color: #e8f4ff;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
        font-size: 22px;
        font-weight: 600;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎓 CUI GPA & CGPA Calculator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Calculate semester-wise GPA and overall CGPA</div>', unsafe_allow_html=True)

# ---------------- Main Input ----------------
num_semesters = st.number_input("Enter number of semesters completed:", min_value=1, max_value=12, step=1)

semester_gpas = []
semester_credits = []

for sem in range(1, int(num_semesters) + 1):
    st.markdown(f"## 🏫 Semester {sem}")
    num_subjects = st.number_input(f"Number of subjects in Semester {sem}:", min_value=1, step=1, key=f"sub_count_{sem}")

    marks, total_marks, credits = [], [], []

    for i in range(int(num_subjects)):
        col1, col2, col3 = st.columns(3)
        with col1:
            marks.append(st.number_input(f"Marks (Sub {i+1})", min_value=0, step=1, key=f"marks_{sem}_{i}"))
        with col2:
            total_marks.append(st.number_input(f"Total Marks (Sub {i+1})", min_value=1, value=100, step=1, key=f"total_{sem}_{i}"))
        with col3:
            credits.append(st.number_input(f"Credit Hours (Sub {i+1})", min_value=1, step=1, key=f"credit_{sem}_{i}"))

    if st.button(f"Calculate GPA for Semester {sem}", key=f"btn_{sem}"):
        gpa, df = calculate_gpa(marks, total_marks, credits)
        semester_gpas.append(gpa)
        semester_credits.append(sum(credits))
        st.dataframe(df, use_container_width=True)
        st.markdown(f'<div class="result-box">📘 Semester {sem} GPA: {gpa}</div>', unsafe_allow_html=True)

# ---------------- CGPA Calculation ----------------
if len(semester_gpas) > 0 and st.button("Calculate Overall CGPA", use_container_width=True):
    cgpa = calculate_cgpa(semester_gpas, semester_credits)
    st.markdown(f'<div class="result-box">🎯 Your Overall CGPA: {cgpa}</div>', unsafe_allow_html=True)
