[33mcommit 8fd868583e711b71119863e6740ec1ebf89cfa37[m[33m ([m[1;36mHEAD[m[33m -> [m[1;32mmain[m[33m)[m
Author: Ujwal-Nandanwar <ujwalnandanwar20@gmail.com>
Date:   Fri Oct 31 17:05:24 2025 +0530

    Improved gantt and pie chart, minor editing

[1mdiff --git a/app.py b/app.py[m
[1mindex 7fb30d5..4a5314e 100644[m
[1m--- a/app.py[m
[1m+++ b/app.py[m
[36m@@ -75,30 +75,43 @@[m [mif st.button("Generate Study Plan"):[m
         selected_labels = [][m
         selected_values = [][m
         selected_colors = [][m
[32m+[m[32m        color_palette = px.colors.qualitative.Safe  # distinct readable colors[m
[32m+[m[32m        color_count = 0[m
 [m
         for topic, time_req, imp, frac in selected_topics:[m
             if frac > 0:  # include both full (1.0) and partial (<1.0)[m
[31m-                selected_labels.append(topic)[m
[32m+[m[32m                selected_labels.append(f"{topic} ({frac*100:.0f}%)")[m
                 selected_values.append(time_req * frac)[m
[32m+[m
                 if frac == 1.0:[m
                     selected_colors.append("green")[m
[31m-                else:[m
[32m+[m[32m                elif frac < 1.0:[m
                     selected_colors.append("gold")[m
[32m+[m[32m                else:[m
[32m+[m[32m                    selected_colors.append(color_palette[color_count % len(color_palette)])[m
[32m+[m[32m                color_count += 1[m
[32m+[m
[32m+[m[32m        if selected_labels:[m
[32m+[m[32m            pie_chart = go.Figure(go.Pie([m
[32m+[m[32m                labels=selected_labels,[m
[32m+[m[32m                values=selected_values,[m
[32m+[m[32m                marker=dict(colors=selected_colors, line=dict(color='black', width=1)),[m
[32m+[m[32m                textinfo="label+percent",[m
[32m+[m[32m                hoverinfo="label+value+percent",[m
[32m+[m[32m                hole=0.3[m
[32m+[m[32m            ))[m
[32m+[m[32m            pie_chart.update_layout(title="🥧 Time Allocation (Selected & Partial Topics Only)")[m
[32m+[m[32m        else:[m
[32m+[m[32m            pie_chart = go.Figure()[m
[32m+[m[32m            pie_chart.update_layout(title="🥧 No topics selected")[m
 [m
[31m-        pie_chart = go.Figure(go.Pie([m
[31m-            labels=selected_labels,[m
[31m-            values=selected_values,[m
[31m-            marker=dict(colors=selected_colors),[m
[31m-            hoverinfo="label+percent",[m
[31m-            textinfo="value+percent",[m
[31m-            hole=0.3[m
[31m-        ))[m
[31m-        pie_chart.update_layout(title="Time Allocation (Selected Topics Only)")[m
[31m-[m
[31m-        # --- GANTT CHART ---[m
[31m-        gantt_html = create_gantt_html(selected_topics, interval)[m
[31m-        st.markdown("### 🟩🟨🟥 Study Schedule Visualization")[m
[31m-        st.components.v1.html(gantt_html, height=600, scrolling=True)[m
[32m+[m[32m        # --- GANTT CHART (Fraction-based Duration + Random Order) ---[m
[32m+[m[32m        try:[m
[32m+[m[32m            gantt_html = create_gantt_html(selected_topics, interval)[m
[32m+[m[32m            st.markdown("### 🕒 Study Schedule Visualization (Gantt Chart)")[m
[32m+[m[32m            st.components.v1.html(gantt_html, height=600, scrolling=True)[m
[32m+[m[32m        except Exception as e:[m
[32m+[m[32m            st.error(f"Gantt chart generation failed: {e}")[m
 [m
         # --- Show Charts ---[m
         col1, col2 = st.columns(2)[m
[36m@@ -107,4 +120,4 @@[m [mif st.button("Generate Study Plan"):[m
         with col2:[m
             st.plotly_chart(pie_chart, use_container_width=True)[m
 [m
[31m-        st.success("✅ Study Plan Generated Successfully!")[m
[32m+[m[32m        st.success("✅ Study Plan Generated Successfully!")[m
\ No newline at end of file[m
[1mdiff --git a/planner/__pycache__/scheduler.cpython-313.pyc b/planner/__pycache__/scheduler.cpython-313.pyc[m
[1mindex fb72355..6210a83 100644[m
Binary files a/planner/__pycache__/scheduler.cpython-313.pyc and b/planner/__pycache__/scheduler.cpython-313.pyc differ
[1mdiff --git a/planner/scheduler.py b/planner/scheduler.py[m
[1mindex 2a0d534..4c7cf76 100644[m
[1m--- a/planner/scheduler.py[m
[1m+++ b/planner/scheduler.py[m
[36m@@ -1,81 +1,86 @@[m
[31m-import pandas as pd[m
 import plotly.graph_objects as go[m
[31m-import plotly.express as px[m
[32m+[m[32mimport pandas as pd[m
 import random[m
 [m
[31m-def create_gantt_html(selected_topics, interval=3):[m
[32m+[m[32mdef create_gantt_html(selected_topics, interval):[m
     """[m
[31m-    Generate a Gantt-style schedule with randomized study order.[m
[31m-    Ensures no two consecutive topics are the same.[m
[32m+[m[32m    Creates an interval-based, non-repetitive Gantt chart (in hours).[m
[32m+[m[32m    Each topic is divided into smaller blocks based on interval size.[m
     """[m
     if not selected_topics:[m
[31m-        return "<p>No topics selected for schedule.</p>"[m
[31m-[m
[31m-    schedule = [][m
[31m-    current_time = 0[m
[31m-    remaining = {t: time_req for t, time_req, _, frac in selected_topics if frac > 0}[m
[32m+[m[32m        return "<p>No topics selected for schedule visualization.</p>"[m
 [m
[31m-    # --- Randomized round-robin logic ---[m
[31m-    last_topic = None[m
[31m-    while any(remaining.values()):[m
[31m-        # Get topics that still need time[m
[31m-        available = [t for t in remaining if remaining[t] > 0 and t != last_topic][m
[32m+[m[32m    # Build expanded list of topics based on fractional time[m
[32m+[m[32m    expanded = [][m
[32m+[m[32m    for topic, time_req, imp, frac in selected_topics:[m
[32m+[m[32m        if frac > 0:[m
[32m+[m[32m            total_time = time_req * frac[m
[32m+[m[32m            expanded.append({"topic": topic, "remaining": total_time})[m
 [m
[31m-        if not available:  # All remaining are same as last, so reset[m
[31m-            available = [t for t in remaining if remaining[t] > 0][m
[32m+[m[32m    if not expanded:[m
[32m+[m[32m        return "<p>No valid topics to schedule.</p>"[m
 [m
[31m-        # Randomly pick one from available[m
[31m-        topic = random.choice(available)[m
[32m+[m[32m    tasks = [][m
[32m+[m[32m    current_time = 0[m
[32m+[m[32m    prev_topic = None[m
[32m+[m[32m    random.shuffle(expanded)[m
 [m
[31m-        # Get details from selected_topics[m
[31m-        for t, time_req, imp, frac in selected_topics:[m
[31m-            if t == topic:[m
[31m-                break[m
[32m+[m[32m    # Generate interval-based schedule[m
[32m+[m[32m    while any(t["remaining"] > 0 for t in expanded):[m
[32m+[m[32m        available = [t for t in expanded if t["remaining"] > 0 and t["topic"] != prev_topic][m
[32m+[m[32m        if not available:[m
[32m+[m[32m            available = [t for t in expanded if t["remaining"] > 0][m
 [m
[31m-        study_time = min(interval, remaining[topic])[m
[31m-        start_time = current_time[m
[31m-        end_time = start_time + study_time[m
[32m+[m[32m        chosen = random.choice(available)[m
[32m+[m[32m        topic = chosen["topic"][m
[32m+[m[32m        time_slice = min(interval, chosen["remaining"])[m
[32m+[m[32m        start = current_time[m
[32m+[m[32m        end = start + time_slice[m
 [m
[31m-        schedule.append({[m
[32m+[m[32m        tasks.append({[m
             "Topic": topic,[m
[31m-            "Start": start_time,[m
[31m-            "End": end_time,[m
[31m-            "Hours": study_time[m
[32m+[m[32m            "Start": start,[m
[32m+[m[32m            "Finish": end[m
         })[m
 [m
[31m-        remaining[topic] -= study_time[m
[31m-        current_time = end_time[m
[31m-        last_topic = topic  # Track last studied topic[m
[32m+[m[32m        chosen["remaining"] -= time_slice[m
[32m+[m[32m        current_time += time_slice[m
[32m+[m[32m        prev_topic = topic[m
 [m
[31m-    df = pd.DataFrame(schedule)[m
[31m-    if df.empty:[m
[31m-        return "<p>No study schedule could be generated.</p>"[m
[32m+[m[32m    df = pd.DataFrame(tasks)[m
 [m
[31m-    # --- Gantt chart (stacked horizontal bars) ---[m
[32m+[m[32m    # ✅ Prevent Plotly from converting to dates by using graph_objects[m
     fig = go.Figure()[m
[31m-    unique_topics = df['Topic'].unique()[m
[31m-    colors = px.colors.qualitative.Safe  # softer, distinct palette[m
 [m
[31m-    for i, topic in enumerate(unique_topics):[m
[31m-        topic_data = df[df['Topic'] == topic][m
[31m-        for _, row in topic_data.iterrows():[m
[31m-            fig.add_trace(go.Bar([m
[31m-                x=[row['Hours']],[m
[31m-                y=[topic],[m
[31m-                orientation='h',[m
[31m-                base=[row['Start']],[m
[31m-                name=topic,[m
[31m-                marker=dict(color=colors[i % len(colors)]),[m
[31m-                hovertemplate=f"Topic: {topic}<br>Start: {row['Start']}h<br>End: {row['End']}h<br>Duration: {row['Hours']}h<extra></extra>"[m
[31m-            ))[m
[32m+[m[32m    # Assign consistent random colors[m
[32m+[m[32m    palette = [[m
[32m+[m[32m        "#4CAF50", "#2196F3", "#FFC107", "#9C27B0", "#FF5722",[m
[32m+[m[32m        "#00BCD4", "#E91E63", "#8BC34A", "#FF9800", "#795548"[m
[32m+[m[32m    ][m
[32m+[m[32m    color_map = {}[m
[32m+[m[32m    color_index = 0[m
[32m+[m
[32m+[m[32m    for _, row in df.iterrows():[m
[32m+[m[32m        topic = row["Topic"][m
[32m+[m[32m        if topic not in color_map:[m
[32m+[m[32m            color_map[topic] = palette[color_index % len(palette)][m
[32m+[m[32m            color_index += 1[m
[32m+[m
[32m+[m[32m        fig.add_trace(go.Bar([m
[32m+[m[32m            x=[row["Finish"] - row["Start"]],[m
[32m+[m[32m            y=[topic],[m
[32m+[m[32m            base=row["Start"],[m
[32m+[m[32m            orientation='h',[m
[32m+[m[32m            marker=dict(color=color_map[topic]),[m
[32m+[m[32m            hovertemplate=f"{topic}<br>{row['Start']}–{row['Finish']} hrs<extra></extra>"[m
[32m+[m[32m        ))[m
 [m
     fig.update_layout([m
[31m-        title="Personalized Study Schedule (Randomized Gantt Chart)",[m
[31m-        xaxis_title="Total Study Time (hours)",[m
[31m-        yaxis_title="Topics",[m
[32m+[m[32m        title="📅 Interval-Based Study Schedule (Gantt Chart)",[m
         barmode='stack',[m
[31m-        template="plotly_white",[m
[31m-        height=550,[m
[32m+[m[32m        xaxis=dict(title="Time (hours)", type="linear", tick0=0, dtick=1),[m
[32m+[m[32m        yaxis=dict(title="Topics", autorange="reversed"),[m
[32m+[m[32m        height=600,[m
         showlegend=False[m
     )[m
 [m
