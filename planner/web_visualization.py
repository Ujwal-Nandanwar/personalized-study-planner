from flask import Flask, render_template
import plotly.graph_objects as go
import webbrowser
import threading
from planner.scheduler import create_gantt_html

app = Flask(__name__, template_folder="../templates")

# Global variable to hold data passed from main.py
DATA = {}

@app.route('/')
def index():
    try:
        topics = DATA.get('topics', [])
        importance = DATA.get('importance', [])
        time_required = DATA.get('time_required', [])
        selected = DATA.get('selected', [])
        partial_selected = DATA.get('partial_selected', [])
        interval = DATA.get('interval', 3)

        if not topics or not importance:
            return "<h2>No data received from main program.</h2>"

        # Extract topic names for clarity
        selected_topics = [t for t, _, _, _ in selected]
        partial_topics = [t for t, _, _, frac in (partial_selected or []) if 0 < frac < 1]

        
        # BAR CHART
        colors = []
        for topic in topics:
            if topic in selected_topics:
                colors.append("green")
            elif topic in partial_topics:
                colors.append("gold")
            else:
                colors.append("red")

        bar_chart = go.Figure()
        bar_chart.add_trace(go.Bar(
            x=topics,
            y=importance,
            marker_color=colors,
            hovertemplate="Topic: %{x}<br>Importance: %{y}<extra></extra>"
        ))
        bar_chart.update_layout(
            title="Topic Importance Overview",
            xaxis_title="Topics",
            yaxis_title="Importance",
            template="plotly_white",
            height=450
        )
        bar_html = bar_chart.to_html(full_html=False)

        # PIE CHART
        labels, values, pie_colors = [], [], []
        for topic, time in zip(topics, time_required):
            labels.append(topic)
            values.append(time)
            if topic in selected_topics:
                pie_colors.append("green")
            elif topic in partial_topics:
                pie_colors.append("gold")
            else:
                pie_colors.append("red")

        pie_chart = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=pie_colors),
            hoverinfo="label+percent",
            textinfo="value+percent",
            hole=0.3
        )])
        pie_chart.update_layout(
            title="Time Allocation by Topic",
            template="plotly_white",
            height=450
        )
        pie_html = pie_chart.to_html(full_html=False)

        #  GANTT CHART
        gantt_html = create_gantt_html(DATA.get('selected_topics', []), interval)

        # Render all in HTML
        return render_template(
            'output.html',
            bar_html=bar_html,
            pie_html=pie_html,
            gantt_html=gantt_html
        )

    except Exception as e:
        print("Error in Flask route:", e)
        return f"<h3>Server Error:</h3><pre>{e}</pre>"


# -------------------------------------------------------------------------
# 🌐 Function to Start Flask + Auto-Open Browser
# -------------------------------------------------------------------------
def show_web_visual(topics, time_required, importance, selected, selected_topics, interval, partial_selected=None):
    global DATA
    DATA = {
        'topics': topics,
        'time_required': time_required,
        'importance': importance,
        'selected': selected,
        'selected_topics': selected_topics,
        'partial_selected': partial_selected,
        'interval': interval
    }

    # Automatically open dashboard
    def open_browser():
        webbrowser.open("http://127.0.0.1:5000/", new=2)  # new=2 → open in new tab

    threading.Timer(1, open_browser).start()
    app.run(debug=False, use_reloader=False)
