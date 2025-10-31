import plotly.graph_objects as go
import pandas as pd
import random

def create_gantt_html(selected_topics, interval):
    """
    Creates an interval-based, non-repetitive Gantt chart (in hours).
    Each topic is divided into smaller blocks based on interval size.
    """
    if not selected_topics:
        return "<p>No topics selected for schedule visualization.</p>"

    # Build expanded list of topics based on fractional time
    expanded = []
    for topic, time_req, imp, frac in selected_topics:
        if frac > 0:
            total_time = time_req * frac
            expanded.append({"topic": topic, "remaining": total_time})

    if not expanded:
        return "<p>No valid topics to schedule.</p>"

    tasks = []
    current_time = 0
    prev_topic = None
    random.shuffle(expanded)

    # Generate interval-based schedule
    while any(t["remaining"] > 0 for t in expanded):
        available = [t for t in expanded if t["remaining"] > 0 and t["topic"] != prev_topic]
        if not available:
            available = [t for t in expanded if t["remaining"] > 0]

        chosen = random.choice(available)
        topic = chosen["topic"]
        time_slice = min(interval, chosen["remaining"])
        start = current_time
        end = start + time_slice

        tasks.append({
            "Topic": topic,
            "Start": start,
            "Finish": end
        })

        chosen["remaining"] -= time_slice
        current_time += time_slice
        prev_topic = topic

    df = pd.DataFrame(tasks)

    # ✅ Prevent Plotly from converting to dates by using graph_objects
    fig = go.Figure()

    # Assign consistent random colors
    palette = [
        "#4CAF50", "#2196F3", "#FFC107", "#9C27B0", "#FF5722",
        "#00BCD4", "#E91E63", "#8BC34A", "#FF9800", "#795548"
    ]
    color_map = {}
    color_index = 0

    for _, row in df.iterrows():
        topic = row["Topic"]
        if topic not in color_map:
            color_map[topic] = palette[color_index % len(palette)]
            color_index += 1

        fig.add_trace(go.Bar(
            x=[row["Finish"] - row["Start"]],
            y=[topic],
            base=row["Start"],
            orientation='h',
            marker=dict(color=color_map[topic]),
            hovertemplate=f"{topic}<br>{row['Start']}–{row['Finish']} hrs<extra></extra>"
        ))

    fig.update_layout(
        title="📅 Interval-Based Study Schedule (Gantt Chart)",
        barmode='stack',
        xaxis=dict(title="Time (hours)", type="linear", tick0=0, dtick=1),
        yaxis=dict(title="Topics", autorange="reversed"),
        height=600,
        showlegend=False
    )

    return fig.to_html(full_html=False)
