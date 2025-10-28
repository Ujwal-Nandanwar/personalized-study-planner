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

        if not topics or not importance:
            return "<h2>No data received from main program.</h2>"

        # --- Bar Chart ---
        bar_chart = go.Figure()
        colors = ['green' if i in selected else 'red' for i in range(len(topics))]
        bar_chart.add_trace(go.Bar(x=topics, y=importance, marker_color=colors))
        bar_chart.update_layout(title="Topic Importance Chart",
                                xaxis_title="Topic", yaxis_title="Importance")

        # --- Pie Chart ---
        if selected:
            chosen = [topics[i] for i in selected]
            chosen_time = [time_required[i] for i in selected]
        else:
            chosen = topics
            chosen_time = time_required

        pie_chart = go.Figure(data=[go.Pie(labels=chosen, values=chosen_time, hole=0.4)])
        pie_chart.update_layout(title="Time Distribution (Chosen Topics)")

        bar_html = bar_chart.to_html(full_html=False)
        pie_html = pie_chart.to_html(full_html=False)
        # --- Gantt Chart (Schedule Visualization) ---
        gantt_html = create_gantt_html(DATA.get('selected_topics', []), DATA.get('interval', 3))

        return render_template('output.html', bar_html=bar_html, pie_html=pie_html, gantt_html=gantt_html)
    except Exception as e:
        # Print full error for debugging
        print("Error in Flask route:", e)
        return f"<h3>Server Error:</h3><pre>{e}</pre>"

#def open_browser():
#    webbrowser.open("http://127.0.0.1:5000/")

#def show_web_visual(topics, time_required, importance, selected):
#    global DATA
#    DATA = {
#        'topics': topics,
#        'time_required': time_required,
#        'importance': importance,
#        'selected': selected
#    }
#    threading.Timer(1, open_browser).start()
#    app.run(debug=False, use_reloader=False)

def show_web_visual(topics, time_required, importance, selected, selected_topics):
    global DATA
    DATA = {
        'topics': topics,
        'time_required': time_required,
        'importance': importance,
        'selected': selected,
        'selected_topics': selected_topics
    }

    # --- automatically open the dashboard in browser ---
    def open_browser():
        webbrowser.open("http://127.0.0.1:5000/", new=2)   # new=2 → open new tab

    # Start Flask and open browser after 1 second
    threading.Timer(1, open_browser).start()
    app.run(debug=False, use_reloader=False)

