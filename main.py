import streamlit as st
import pandas as pd
import io

# ----------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------
st.set_page_config(page_title="CUI GPA & CGPA Calculator", layout="wide")

# Dark theme styling
st.markdown("""
    <style>
    body {background-color:#0E1117; color:#FAFAFA;}
    .stApp {background-color:#0E1117;}
    div[data-testid="stMetricValue"] {
        font-size:28px; color:#4CAF50; font-weight:bold;
    }
    .css-1v3fvcr {background-color:#1E1E1E;}
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# HEADER
# ----------------------------------------------------------
st.title("🎓 CUI GPA & CGPA Calculator")
st.caption("Based on the official **CUI / HEC Grading Criteria** (Notification: Dec 7, 2020)")

# ----------------------------------------------------------
# GRADE MAPPING
# ----------------------------------------------------------
def get_grade_point(percentage):
    if percentage >= 85: return "A", 4.00
    elif percentage >= 80: return "A-", 3.66
    elif percentage >= 75: return "B+", 3.33
    elif percentage >= 71: return "B", 3.00
    elif percentage >= 68: return "B-", 2.66
    elif percentage >= 64: return "C+", 2.33
    elif percentage >= 61: return "C", 2.00
    elif percentage >= 58: return "C-", 1.66
    elif percentage >= 54: return "D+", 1.30
    elif percentage >= 50: return "D", 1.00
    else: return "F", 0.00

# ----------------------------------------------------------
# HELPER FUNCTIONS
# ----------------------------------------------------------
def calculate_semester_gpa(subject_data):
    total_points, total_credits = 0, 0
    for sub in subject_data:
        total_points += sub["Grade Point"] * sub["Credit Hours"]
        total_credits += sub["Credit Hours"]
    if total_credits == 0:
        return 0
    return round(total_points / total_credits, 2)

def calculate_cgpa(all_semesters):
    total_points, total_credits = 0, 0
    for sem in all_semesters:
        total_points += sem["GPA"] * sem["Total Credits"]
        total_credits += sem["Total Credits"]
    if total_credits == 0:
        return 0
    return round(total_points / total_credits, 2)

# ----------------------------------------------------------
# USER INPUT SECTION
# ----------------------------------------------------------
st.subheader("📘 Enter Academic Details")

current_sem = st.number_input("Enter your current semester (1–8):", min_value=1, max_value=8, step=1)
all_semesters = []

# ----------------------------------------------------------
# SEMESTER INPUT LOOP
# ----------------------------------------------------------
for sem in range(1, current_sem + 1):
    with st.expander(f"🧾 Semester {sem} Details", expanded=(sem == current_sem)):
        num_subjects = st.number_input(
            f"Number of subjects in Semester {sem}:",
            min_value=1, step=1, key=f"subs_{sem}"
        )

        subjects = []
        for i in range(1, num_subjects + 1):
            marks = st.number_input(f"Marks obtained (Subject {i})", 0.0, 100.0, key=f"m_{sem}_{i}")
            total = st.number_input(f"Total marks (Subject {i})", 1.0, 100.0, value=100.0, key=f"t_{sem}_{i}")
            credit = st.number_input(f"Credit hours (Subject {i})", 1.0, 5.0, key=f"c_{sem}_{i}")
            
            percentage = (marks / total) * 100
            grade, gp = get_grade_point(percentage)
            subjects.append({
                "Subject": f"Subject {i}",
                "Marks": f"{marks:.0f}/{int(total)}",
                "Percentage": f"{percentage:.2f}%",
                "Grade": grade,
                "Grade Point": gp,
                "Credit Hours": credit
            })

        # Show semester details table
        df = pd.DataFrame(subjects)
        st.dataframe(df, use_container_width=True)

        # Calculate GPA
        sem_gpa = calculate_semester_gpa(subjects)
        total_credits = sum([s["Credit Hours"] for s in subjects])
        all_semesters.append({"Semester": sem, "GPA": sem_gpa, "Total Credits": total_credits})
        st.success(f"🎯 GPA for Semester {sem}: {sem_gpa}")

# ----------------------------------------------------------
# CALCULATE & DISPLAY CGPA
# ----------------------------------------------------------
if st.button("📊 Calculate Overall CGPA"):
    if all_semesters:
        cgpa = calculate_cgpa(all_semesters)
        st.markdown("---")
        st.metric(label=f"🌟 Overall CGPA after Semester {current_sem}", value=f"{cgpa:.2f}")

        sem_summary = pd.DataFrame(all_semesters)
        st.dataframe(sem_summary, use_container_width=True)

        # --------------------------------------------------
        # DOWNLOAD OPTION (EXCEL)
        # --------------------------------------------------
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            sem_summary.to_excel(writer, index=False, sheet_name="CGPA Summary")
            for sem in range(1, current_sem + 1):
                writer.sheets["CGPA Summary"].set_column("A:C", 20)
        excel_data = output.getvalue()

        st.download_button(
            label="⬇️ Download CGPA Report (Excel)",
            data=excel_data,
            file_name=f"CUI_CGPA_Report_Sem{current_sem}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.error("Please fill in at least one semester before calculating CGPA.")
