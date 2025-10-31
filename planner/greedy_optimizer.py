import time

def greedy_study_plan(topics, time_required, importance, total_available_time):
    
    n = len(topics)
    items = []

    # Creating list of (topic, time, importance, ratio)
    for i in range(n):
        ratio = importance[i] / time_required[i]
        items.append((topics[i], time_required[i], importance[i], ratio))

    items.sort(key=lambda x: x[3], reverse=True)  #Sorting 

    total_importance = 0.0
    used_time = 0.0
    selected_topics = []
    full_selected = []
    partial_selected = []
    
    start = time.time()

    for topic, time_req, imp, ratio in items:
        if used_time >= total_available_time:
            break
        if used_time + time_req <= total_available_time:
            used_time += time_req
            total_importance += imp
            selected_topics.append((topic, time_req, imp, 1.0))  # fully studied
            full_selected.append((topic, time_req, imp, 1.0))
        else:
            remain = total_available_time - used_time           
            fraction = remain / time_req
            total_importance += imp * fraction
            used_time += remain
            selected_topics.append((topic, time_req, imp, fraction))    # partially studied
            partial_selected.append((topic, time_req, imp, fraction))
            break

    end = time.time()

    print("\n📘 Optimal Study Plan (Greedy - Importance/Time Ratio):")
    for t, tm, imp, frac in selected_topics:
        print(f"  - {t}: {frac*100:.1f}% studied ({tm*frac:.1f} hrs) → {imp*frac:.1f} importance")

    print(f"\n✅ Total Importance Gained: {total_importance:.2f}")
    print(f"⏱️ Total Time Used: {used_time:.2f} hrs (of {total_available_time})")
    print(f"⚡ Time Taken for Computation: {round(end - start, 6)} sec")

   
    return selected_topics, full_selected, partial_selected
