import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import random

def create_gantt_html(selected_topics, interval=3):
    """
    Generate a Gantt-style schedule with randomized study order.
    Ensures no two consecutive topics are the same.
    """
    if not selected_topics:
        return "<p>No topics selected for schedule.</p>"

    schedule = []
    current_time = 0
    remaining = {t: time_req for t, time_req, _, frac in selected_topics if frac > 0}

    # --- Randomized round-robin logic ---
    last_topic = None
    while any(remaining.values()):
        # Get topics that still need time
        available = [t for t in remaining if remaining[t] > 0 and t != last_topic]

        if not available:  # All remaining are same as last, so reset
            available = [t for t in remaining if remaining[t] > 0]

        # Randomly pick one from available
        topic = random.choice(available)

        # Get details from selected_topics
        for t, time_req, imp, frac in selected_topics:
            if t == topic:
                break

        study_time = min(interval, remaining[topic])
        start_time = current_time
        end_time = start_time + study_time

        schedule.append({
            "Topic": topic,
            "Start": start_time,
            "End": end_time,
            "Hours": study_time
        })

        remaining[topic] -= study_time
        current_time = end_time
        last_topic = topic  # Track last studied topic

    df = pd.DataFrame(schedule)
    if df.empty:
        return "<p>No study schedule could be generated.</p>"

    # --- Gantt chart (stacked horizontal bars) ---
    fig = go.Figure()
    unique_topics = df['Topic'].unique()
    colors = px.colors.qualitative.Safe  # softer, distinct palette

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
        title="Personalized Study Schedule (Randomized Gantt Chart)",
        xaxis_title="Total Study Time (hours)",
        yaxis_title="Topics",
        barmode='stack',
        template="plotly_white",
        height=550,
        showlegend=False
    )

    return fig.to_html(full_html=False)
