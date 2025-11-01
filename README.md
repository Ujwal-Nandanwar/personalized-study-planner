# 🎓 Personalized Study Planner

A smart and interactive **study planning tool** built using Python and **Greedy Algorithm (Fractional Knapsack)**.  
It helps students organize their study schedule efficiently based on topic importance and available study time.

---

## 🚀 Live Demo

👉 **[Click here to open the Study Planner](https://personalized-study-planner.streamlit.app/)**  

(Hosted on [Streamlit Cloud](https://streamlit.io))

---

## 🧠 About the Project

This project optimizes your study schedule using a **Greedy-based Fractional Knapsack approach**.  
Each topic has:
- Estimated study time ⏱️  
- Importance level ⭐  

The algorithm selects topics that maximize total learning importance within the available time.  
Partially studied topics are also included proportionally.

It also visualizes your plan using:
- 📊 **Bar Chart:** Shows topic importance and selection status  
- 🥧 **Pie Chart:** Displays selected and partially selected topics only  
- 🕒 **Gantt Chart:** Visualizes the randomized non-repetitive study timeline  

---

## 🧩 Features

✅ Manual or CSV-based topic input  
✅ Greedy optimization (importance/time ratio)  
✅ Auto-generated Gantt Chart  
✅ Color-coded visualization:
- 🟩 Fully selected topics  
- 🟨 Partially selected topics  
- 🟥 Not selected topics  
✅ Hosted with Streamlit for easy access anywhere  

---

## ⚙️ Tech Stack

| Component | Technology |
|------------|-------------|
| **Frontend/UI** | Streamlit |
| **Backend Logic** | Python |
| **Visualization** | Plotly |
| **Algorithm** | Greedy (Fractional Knapsack) |

---

## 📂 Folder Structure

```
personalized-study-planner/
│
├── app.py                    # Main Streamlit app
├── planner/
│   ├── greedy_optimizer.py    # Greedy algorithm logic
│   ├── scheduler.py           # Gantt chart and scheduling
│
├── requirements.txt           # Dependencies for Streamlit Cloud
└── README.md                  # Project documentation
```

---

## 🧾 Example CSV Format

If you upload a CSV, it should look like this:

| Topic | TimeRequired | Importance |
|--------|---------------|------------|
| Data Structures | 5 | 9 |
| Operating Systems | 4 | 8 |
| DAA | 6 | 10 |

---

## 🧑‍💻 How to Run Locally

```bash
# 1. Clone this repository
git clone https://github.com/Ujwal-Nandanwar/personalized-study-planner.git

# 2. Move into the project folder
cd personalized-study-planner

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

Then open the browser link shown in your terminal.

---

## 🔗 Quick Access

🌐 **Live App:** [https://personalized-study-planner.streamlit.app/](https://personalized-study-planner.streamlit.app/)  
📁 **GitHub Repo:** [https://github.com/Ujwal-Nandanwar/personalized-study-planner](https://github.com/Ujwal-Nandanwar/personalized-study-planner)
