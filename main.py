import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ---------------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------------
st.set_page_config(page_title="🎓 GPA & CGPA Calculator", layout="wide")

# Custom CSS Styling (Dark Mode + Accent)
st.markdown("""
    <style>
        .main {
            background-color: #0E1117;
            color: #F5F5F5;
        }
        h1, h2, h3 {
            color: #00FFCC;
        }
        .stTabs [role="tablist"] {
            justify-content: center;
        }
        .stTabs [role="tab"] {
            background: #1C1F26;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            margin-right: 5px;
        }
        .stTabs [aria-selected="true"] {
            background-color: #00FFCC !important;
            color: #000000 !important;
            font-weight: bold !important;
        }
        div[data-testid="stExpander"] {
            background-color: #161A22;
            border-radius: 10px;
            border: 1px solid #00FFCC;
            padding: 10px;
        }
        .stButton>button {
            background-color: #00FFCC;
            color: black;
            border-radius: 10px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------
def calculate_grade_point(marks_obtained, total_marks):
    """Convert percentage to grade points"""
    percentage = (marks_obtained / total_marks) * 100
    if percentage >= 85:
        return 4.0
    elif percentage >= 80:
        return 3.7
    elif percentage >= 75:
        return 3.3
    elif percentage >= 70:
        return 3.0
    elif percentage >= 65:
        return 2.7
    elif percentage >= 60:
        return 2.3
    elif percentage >= 55:
        return 2.0
    elif percentage >= 50:
        return 1.7
    else:
        return 0.0


def calculate_gpa(marks, totals, credits):
    """Calculate semester GPA"""
    total_points = sum(calculate_grade_point(m, t) * c for m, t, c in zip(marks, totals, credits))
    total_credits = sum(credits)
    if total_credits == 0:
        return 0
    return round(total_points / total_credits, 2)


def calculate_cgpa(all_gpas, all_credits):
    """Weighted average of all semester GPAs"""
    total_weighted_points = sum(g * c for g, c in zip(all_gpas, all_credits))
    total_credits = sum(all_credits)
    if total_credits == 0:
        return 0
    return round(total_weighted_points / total_credits, 2)


# ---------------------------------------------------------------
# MAIN APP
# ---------------------------------------------------------------
st.title("🎓 GPA & CGPA Calculator (Dark Theme Edition)")
st.markdown("Easily calculate GPA for each semester and your overall CGPA — with visual progress tracking!")

num_semesters = st.number_input("Enter total number of semesters completed:", min_value=1, max_value=12, step=1)

semester_gpas = []
semester_credits = []

for sem in range(1, num_semesters + 1):
    with st.expander(f"📘 Semester {sem} Details", expanded=False):
        entry_type = st.radio(
            f"How would you like to enter data for Semester {sem}?",
            ["Enter subjects manually", "Enter GPA directly"],
            key=f"type_{sem}"
        )

        if entry_type == "Enter subjects manually":
            num_subjects = st.number_input(f"Number of subjects in Semester {sem}:", min_value=1, step=1, key=f"subs_{sem}")
            marks, totals, credits = [], [], []

            for i in range(num_subjects):
                st.markdown(f"**Subject {i+1}:**")
                m = st.number_input(f"Marks obtained (Subject {i+1})", min_value=0.0, key=f"m_{sem}_{i}")
                t = st.number_input(f"Total marks (Subject {i+1})", min_value=1.0, key=f"t_{sem}_{i}")
                c = st.number_input(f"Credit hours (Subject {i+1})", min_value=1.0, key=f"c_{sem}_{i}")
                marks.append(m)
                totals.append(t)
                credits.append(c)

            gpa = calculate_gpa(marks, totals, credits)
            total_credits = sum(credits)
            st.success(f"📗 GPA for Semester {sem}: **{gpa}**")
            semester_gpas.append(gpa)
            semester_credits.append(total_credits)

        else:
            gpa = st.number_input(f"Enter GPA for Semester {sem}:", min_value=0.0, max_value=4.0, key=f"gpa_{sem}")
            total_credits = st.number_input(f"Enter total credit hours for Semester {sem}:", min_value=1.0, key=f"cred_{sem}")
            semester_gpas.append(gpa)
            semester_credits.append(total_credits)

# ---------------------------------------------------------------
# RESULTS SECTION
# ---------------------------------------------------------------
if st.button("🔹 Calculate Final CGPA"):
    cgpa = calculate_cgpa(semester_gpas, semester_credits)
    st.markdown("---")
    st.subheader("📊 Results Summary")

    # Create summary DataFrame
    df = pd.DataFrame({
        "Semester": [f"Semester {i+1}" for i in range(num_semesters)],
        "GPA": semester_gpas,
        "Credit Hours": semester_credits
    })
    df["Cumulative CGPA"] = [calculate_cgpa(semester_gpas[:i+1], semester_credits[:i+1]) for i in range(num_semesters)]

    st.dataframe(df, use_container_width=True)

    st.metric(label="🎯 Final CGPA", value=cgpa)

    # Trend detection
    if len(semester_gpas) > 1:
        if semester_gpas[-1] > semester_gpas[-2]:
            st.success("📈 Great! Your GPA improved this semester.")
        elif semester_gpas[-1] < semester_gpas[-2]:
            st.warning("📉 Your GPA decreased this semester. Stay motivated and aim higher!")
        else:
            st.info("➖ Your GPA remained the same as last semester.")

    # Plot GPA Trend
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[f"Sem {i+1}" for i in range(num_semesters)],
        y=semester_gpas,
        mode="lines+markers",
        line=dict(color="#00FFCC", width=3),
        marker=dict(size=10, color="#00FFFF"),
        name="Semester GPA"
    ))
    fig.update_layout(
        title="🎓 GPA Trend Across Semesters",
        xaxis_title="Semester",
        yaxis_title="GPA",
        yaxis=dict(range=[0, 4.2]),
        paper_bgcolor="#0E1117",
        plot_bgcolor="#161A22",
        font=dict(color="white")
    )
    st.plotly_chart(fig, use_container_width=True)

    st.balloons()
