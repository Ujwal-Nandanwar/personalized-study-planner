from planner.input_handler import get_user_input
from planner.dp_algorithm import study_plan_dp
from planner.backtrack import backtrack_solution
from planner.visualization import visualize_plan

def main():
    topics, time_required, importance, total_hours = get_user_input()
    dp = study_plan_dp(time_required, importance, total_hours)
    selected = backtrack_solution(dp, time_required, importance, total_hours)

    print("\n📘 Optimal Study Plan:")
    total_time = sum(time_required[i] for i in selected)
    total_marks = sum(importance[i] for i in selected)
    for i in selected:
        print(f"  - {topics[i]} ({time_required[i]} hrs, {importance[i]} marks)")
    print(f"\nTotal Time: {total_time} hrs | Total Marks: {total_marks}")

    visualize_plan(topics, importance, selected)

if __name__ == "__main__":
    main()
