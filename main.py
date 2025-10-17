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
    total_points = sum(g * c for g, c in zip(gpas, credits_list))
    total_credits = sum(credits_list)
    return round(total_points / total_credits, 2) if total_credits != 0 else 0


# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(page_title="🎓 GPA & CGPA Calculator", layout="wide")

# Dark Theme Styling
st.markdown("""
    <style>
        body {
            background-color: #0e1117;
            color: #fafafa;
        }
        .stApp {
            background-color: #0e1117;
        }
        div.stButton > button {
            background-color: #00b4d8;
            color: white;
            border-radius: 10px;
            height: 3em;
            width: 100%;
            font-size: 16px;
            border: none;
        }
        div.stButton > button:hover {
            background-color: #0096c7;
            color: #ffffff;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #1a1d24;
            color: #ffffff;
            border-radius: 8px;
            margin-right: 5px;
        }
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #0077b6;
        }
        .stTabs [aria-selected="true"] {
            background-color: #00b4d8;
            color: #ffffff;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🎓 GPA & CGPA Calculator (Dark Mode)")

# -----------------------------
# Main Functionality
# -----------------------------
tabs = st.tabs(["🎯 New GPA Calculation", "📘 Use Previous GPA Data"])

with tabs[0]:
    st.subheader("🔹 Enter Semester Details")
    num_semesters = st.number_input("Enter the number of semesters completed (including current):", min_value=1, step=1)

    gpas = []
    credits_list = []
    summary_data = []

    for i in range(int(num_semesters)):
        st.markdown(f"<h4 style='color:#00b4d8;'>Semester {i+1}</h4>", unsafe_allow_html=True)
        num_subjects = st.number_input(f"Number of subjects in Semester {i+1}:", min_value=1, step=1, key=f"subs_{i}")

        marks, total_marks, credits = [], [], []

        for j in range(int(num_subjects)):
            st.write(f"**Subject {j+1}:**")
            marks.append(st.number_input(f"Marks obtained (Subject {j+1})", min_value=0.0, step=1.0, key=f"marks_{i}_{j}"))
            total_marks.append(st.number_input(f"Total marks (Subject {j+1})", min_value=1.0, value=100.0, step=1.0, key=f"total_{i}_{j}"))
            credits.append(st.number_input(f"Credit hours (Subject {j+1})", min_value=1.0, step=1.0, key=f"credit_{i}_{j}"))

        gpa = calculate_gpa(marks, total_marks, credits)
        total_credit = sum(credits)
        gpas.append(gpa)
        credits_list.append(total_credit)

        st.success(f"🎓 GPA for Semester {i+1}: **{gpa}**")

        summary_data.append({
            "Semester": f"Semester {i+1}",
            "GPA": gpa,
            "Credits": total_credit
        })

    if st.button("Calculate CGPA"):
        cgpa = calculate_cgpa(gpas, credits_list)
        st.markdown("---")
        st.success(f"🏆 Your overall CGPA up to Semester {num_semesters} is: **{cgpa}**")

        # Summary Table
        df_summary = pd.DataFrame(summary_data)
        df_summary["Cumulative CGPA"] = [calculate_cgpa(gpas[:i+1], credits_list[:i+1]) for i in range(len(gpas))]
        st.dataframe(df_summary, use_container_width=True)

        # GPA Trend Chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_summary["Semester"],
            y=df_summary["GPA"],
            mode='lines+markers',
            line=dict(color='#00b4d8', width=3),
            marker=dict(size=10, color='#48cae4')
        ))
        fig.update_layout(
            title="📈 GPA Trend Over Semesters",
            xaxis_title="Semester",
            yaxis_title="GPA",
            paper_bgcolor="#0e1117",
            plot_bgcolor="#0e1117",
            font=dict(color="#fafafa"),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

        # Performance Summary
        if len(gpas) > 1:
            if gpas[-1] > gpas[-2]:
                st.info("📈 Great job! Your GPA improved this semester.")
            elif gpas[-1] < gpas[-2]:
                st.warning("📉 Your GPA dropped this semester — keep pushing!")
            else:
                st.info("➖ Your GPA remained consistent this semester.")


# -----------------------------
# Option 2: Use Previous GPA
# -----------------------------
with tabs[1]:
    st.subheader("📘 Enter Previous GPA and Credits")

    num_prev = st.number_input("Enter number of previous semesters:", min_value=1, step=1, key="prev_sem")
    gpas_prev = []
    credits_prev = []

    for i in range(int(num_prev)):
        gpas_prev.append(st.number_input(f"GPA for Semester {i+1}:", min_value=0.0, max_value=4.0, step=0.01, key=f"gpa_prev_{i}"))
        credits_prev.append(st.number_input(f"Total Credit Hours for Semester {i+1}:", min_value=1.0, step=1.0, key=f"cred_prev_{i}"))

    if st.button("Calculate CGPA from Previous Data"):
        cgpa_prev = calculate_cgpa(gpas_prev, credits_prev)
        st.success(f"🏆 Your CGPA based on previous semesters is: **{cgpa_prev}**")
