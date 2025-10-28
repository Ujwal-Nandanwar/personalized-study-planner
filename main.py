import pandas as pd
from planner.input_handler import get_user_input
from planner.dp_algorithm import study_plan_dp
from planner.backtrack import backtrack_solution
from planner.visualization import visualize_plan
from planner.greedy_optimizer import greedy_study_plan
from planner.scheduler import create_gantt_html
from planner.web_visualization import show_web_visual

#def main():
#    topics, time_required, importance, total_hours = get_user_input()
#    dp = study_plan_dp(time_required, importance, total_hours)
#    selected = backtrack_solution(dp, time_required, importance, total_hours)
#
#    print("\n📘 Optimal Study Plan:")
#    total_time = sum(time_required[i] for i in selected)
#    total_marks = sum(importance[i] for i in selected)
#    for i in selected:
#        print(f"  - {topics[i]} ({time_required[i]} hrs, {importance[i]} marks)")
#    print(f"\nTotal Time: {total_time} hrs | Total Marks: {total_marks}")
#
#    visualize_plan(topics, importance, selected)
#
#    # after visualize_plan line
#    show_web_visual(topics, time_required, importance, selected)
    
def get_user_input():
    print("\n📘 Personalized Study Planner Input Options")
    print("1️⃣  Manual Input")
    print("2️⃣  Load from CSV file")
    
    choice = input("Choose an option (1 or 2): ").strip()
    topics, time_required, importance, total_time = [], [], [], 0

    if choice == "1":
        n = int(input("\nEnter number of topics: "))
        for i in range(n):
            topic = input(f"Enter topic {i+1} name: ")
            time_req = float(input(f"Enter time required for {topic} (in hours): "))
            imp = float(input(f"Enter importance/marks weight for {topic}: "))
            topics.append(topic)
            time_required.append(time_req)
            importance.append(imp)

        total_time = float(input("\nEnter your total available study time (in hours): "))

    elif choice == "2":
        path = input("Enter CSV file path (e.g., study_data.csv): ").strip()
        try:
            df = pd.read_csv(path)
            print("\n✅ File loaded successfully!\n")

            if not {'Topic', 'TimeRequired', 'Importance'}.issubset(df.columns):
                print("❌ Error: CSV must contain columns: Topic, TimeRequired, Importance")
                exit()

            topics = df['Topic'].tolist()
            time_required = df['TimeRequired'].astype(float).tolist()
            importance = df['Importance'].astype(float).tolist()

            total_time = float(input("Enter your total available study time (in hours): "))

        except FileNotFoundError:
            print("❌ File not found. Please check the path and try again.")
            exit()
        except Exception as e:
            print("❌ Error reading file:", e)
            exit()

    else:
        print("❌ Invalid choice. Please enter 1 or 2.")
        exit()

    return topics, time_required, importance, total_time


def main():
    topics, time_required, importance, total_time = get_user_input()

    selected, full_selected, partial_selected = greedy_study_plan(
        topics, time_required, importance, total_time
    )

        # Ask for fixed study interval
    interval = float(input("\nEnter fixed study interval (in hours): "))

    # ✅ Create Gantt Chart Schedule
    gantt_html = create_gantt_html(selected, interval)


    # ✅ Web Visualization (Bar + Pie + Ratio)
    show_web_visual(topics, time_required, importance, full_selected, selected)


if __name__ == "__main__":
    main()




