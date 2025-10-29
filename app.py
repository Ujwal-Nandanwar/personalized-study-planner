import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from planner.greedy_optimizer import greedy_study_plan
from planner.scheduler import create_gantt_html
import plotly.express as px
from io import StringIO
import random

st.set_page_config(page_title="Personalized Study Planner", layout="wide")

st.title("📘 Personalized Study Planner")
st.markdown("### Optimize your study time using Greedy (Importance/Time Ratio) Algorithm")

# --- Input method selection ---
input_method = st.radio("Choose input method:", ["Manual Entry", "Upload CSV"])

if input_method == "Manual Entry":
    n = st.number_input("Enter number of topics:", min_value=1, max_value=20, value=3, step=1)
    topics, time_required, importance = [], [], []
    for i in range(n):
        col1, col2, col3 = st.columns(3)
        with col1:
            topic = st.text_input(f"Topic {i+1} name:", key=f"t{i}")
        with col2:
            time_req = st.number_input(f"Time required (hrs) for {topic or f'Topic {i+1}'}:", min_value=1.0, key=f"tr{i}")
        with col3:
            imp = st.number_input(f"Importance (marks/weight) for {topic or f'Topic {i+1}'}:", min_value=1.0, key=f"im{i}")
        topics.append(topic)
        time_required.append(time_req)
        importance.append(imp)
else:
    st.markdown("Upload a CSV with columns: **Topic, TimeRequired, Importance**")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    topics, time_required, importance = [], [], []
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        if not {'Topic', 'TimeRequired', 'Importance'}.issubset(df.columns):
            st.error("❌ CSV must contain columns: Topic, TimeRequired, Importance")
        else:
            topics = df['Topic'].tolist()
            time_required = df['TimeRequired'].astype(float).tolist()
            importance = df['Importance'].astype(float).tolist()
            st.success("✅ CSV uploaded successfully!")

total_time = st.number_input("Enter your total available study time (in hours):", min_value=1.0, value=10.0)
interval = st.number_input("Enter fixed study interval (in hours):", min_value=1.0, value=3.0)

if st.button("Generate Study Plan"):
    if not topics:
        st.error("Please provide topic details or upload a valid CSV.")
    else:
        selected, full_selected, partial_selected = greedy_study_plan(topics, time_required, importance, total_time)

        # Prepare data
        selected_topics = selected
        full_topics = [t for t, _, _, _ in full_selected]
        partial_topics = [t for t, _, _, f in partial_selected if 0 < f < 1]

        # --- BAR CHART ---
        colors = []
        for topic in topics:
            if topic in full_topics:
                colors.append("green")
            elif topic in partial_topics:
                colors.append("gold")
            else:
                colors.append("red")

        bar_chart = go.Figure()
        bar_chart.add_trace(go.Bar(x=topics, y=importance, marker_color=colors))
        bar_chart.update_layout(title="Topic Importance Overview", xaxis_title="Topic", yaxis_title="Importance")

        # --- PIE CHART (Only Selected Topics) ---
        selected_labels = []
        selected_values = []
        selected_colors = []

        for topic, time_req, imp, frac in selected_topics:
            if frac > 0:  # include both full (1.0) and partial (<1.0)
                selected_labels.append(topic)
                selected_values.append(time_req * frac)
                if frac == 1.0:
                    selected_colors.append("green")
                else:
                    selected_colors.append("gold")

        pie_chart = go.Figure(go.Pie(
            labels=selected_labels,
            values=selected_values,
            marker=dict(colors=selected_colors),
            hoverinfo="label+percent",
            textinfo="value+percent",
            hole=0.3
        ))
        pie_chart.update_layout(title="Time Allocation (Selected Topics Only)")

        # --- GANTT CHART ---
        gantt_html = create_gantt_html(selected_topics, interval)
        st.markdown("### 🟩🟨🟥 Study Schedule Visualization")
        st.components.v1.html(gantt_html, height=600, scrolling=True)

        # --- Show Charts ---
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(bar_chart, use_container_width=True)
        with col2:
            st.plotly_chart(pie_chart, use_container_width=True)

        st.success("✅ Study Plan Generated Successfully!")
