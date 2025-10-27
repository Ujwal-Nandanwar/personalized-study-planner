import matplotlib.pyplot as plt

def visualize_plan(topics, importance, selected):
    colors = ['green' if i in selected else 'red' for i in range(len(topics))]
    plt.bar(topics, importance, color=colors)
    plt.title("Personalized Study Plan")
    plt.xlabel("Subjects")
    plt.ylabel("Importance Score")
    plt.show()
