import csv

def get_user_input():
    choice = input("Enter 1 for manual input, 2 for CSV input: ")

    if choice == "2":
        filename = input("Enter CSV file path (e.g., data/sample_input.csv): ")
        topics, time_required, importance = [], [], []
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                topics.append(row['Topic'])
                time_required.append(int(row['Time']))
                importance.append(int(row['Importance']))
    else:
        n = int(input("Enter number of topics: "))
        topics, time_required, importance = [], [], []
        for _ in range(n):
            t = input("Topic name: ")
            h = int(input(f"Hours needed for {t}: "))
            imp = int(input(f"Importance (1-10) of {t}: "))
            topics.append(t)
            time_required.append(h)
            importance.append(imp)

    total_hours = int(input("\nEnter total study hours available: "))
    return topics, time_required, importance, total_hours
