import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def create_gantt_html(selected_topics, interval=3):
    """
    Generate Gantt-style study schedule using horizontal bar chart.
    Each topic gets multiple bars if studied in intervals.
    """
    schedule = []
    current_time = 0
    remaining = {t: time_req for t, time_req, _, frac in selected_topics if frac > 0}

    # Create round-robin schedule
    while any(remaining.values()):
        for t, time_req, imp, frac in selected_topics:
            if remaining[t] <= 0:
                continue
            study_time = min(interval, remaining[t])
            start_time = current_time
            end_time = start_time + study_time
            schedule.append({
                "Topic": t,
                "Start": start_time,
                "End": end_time,
                "Hours": study_time
            })
            remaining[t] -= study_time
            current_time = end_time

    df = pd.DataFrame(schedule)
    if df.empty:
        return "<p>No study schedule could be generated.</p>"

    # --- Create Gantt using horizontal bar chart ---
    fig = go.Figure()
    unique_topics = df['Topic'].unique()
    colors = px.colors.qualitative.Plotly  # distinct colors

    for i, topic in enumerate(unique_topics):
        topic_data = df[df['Topic'] == topic]
        for _, row in topic_data.iterrows():
            fig.add_trace(go.Bar(
                x=[row['Hours']],
                y=[topic],
                orientation='h',
                base=[row['Start']],
                name=topic,
                marker=dict(color=colors[i % len(colors)]),
                hovertemplate=f"Topic: {topic}<br>Start: {row['Start']}h<br>End: {row['End']}h<br>Duration: {row['Hours']}h<extra></extra>"
            ))

    fig.update_layout(
        title="Personalized Study Schedule (Gantt Chart)",
        xaxis_title="Total Study Time (hours)",
        yaxis_title="Topics",
        barmode='stack',
        template="plotly_white",
        height=500,
        showlegend=False
    )

    return fig.to_html(full_html=False)
