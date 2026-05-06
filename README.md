# 🏏 IPL Player Analyzer

An interactive data analytics dashboard built on 
260,000+ ball-by-ball IPL records from 2008 to 2020.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Live-red)

## 🔗 Live Demo
👉 [Click here to open the app](<https://ipl-player-analyzer-t77x2um4gyodxknd66qhwb.streamlit.app/>)

---

## 📌 Problem Statement
IPL generates massive amounts of cricket data — but 
no simple tool exists for fans and analysts to explore 
individual player performance interactively. This project 
bridges that gap with a live analytics dashboard.

---

## 📊 Dataset
| File | Rows | Description |
|------|------|-------------|
| matches.csv | 1,095 | Match-level data — teams, toss, venue, result |
| deliveries.csv | 2,60,920 | Ball-by-ball data — batter, bowler, runs, wickets |

**Source:** Kaggle — IPL Complete Dataset 2008–2020

---

## ⚙️ Features

### 📊 Tab 1 — Player Analyzer
**Batter Analysis:**
- Career stats — Total Runs, Matches, Average, Strike Rate, Highest Score
- Season wise runs trend
- Top 3 performing venues
- Strike Rate vs each IPL team

**Bowler Analysis:**
- Career stats — Total Wickets, Matches, Economy, Avg Wickets/Match, Best Match
- Season wise wickets trend
- Top 3 venues — most wickets
- Wickets vs each IPL team

### ⚔️ Tab 2 — Head to Head
- Select any Batter vs any Bowler
- See balls faced, runs scored, times dismissed
- Strike rate, dot ball %, boundaries
- Verdict — 🟢 Batter Dominates / 🔴 Bowler Dominates / 🟡 Competitive

---

## 🔬 Project Workflow

```
Data Loading → Cleaning → EDA → Feature Engineering
→ ML Attempt → Player Analytics → Streamlit Deployment
```

### Data Cleaning
- Standardized team names — Delhi Daredevils → Delhi Capitals etc
- Handled missing values across 8+ columns
- Fixed venue naming inconsistencies
- Removed leakage columns before modelling

### EDA — Key Findings
- Mumbai Indians most successful team — 130+ wins
- Fielding first wins more matches — chasing advantage
- Virat Kohli — all time leading IPL run scorer
- Yuzvendra Chahal — all time leading wicket taker
- Toss winning teams win only ~55% — minimal advantage

### Feature Engineering
- `strike_rate` — batsman runs per 100 balls
- `economy` — runs conceded per over

### ML Experiment
Attempted match winner prediction — best accuracy 55% 
consistent with industry benchmark for cricket prediction. 
Shifted to player performance analysis for more 
meaningful and actionable insights.

---

## 🛠️ Tech Stack

| Tool | Usage |
|------|-------|
| Python | Core language |
| Pandas | Data manipulation |
| Matplotlib | Visualizations |
| Scikit-learn | ML Pipeline |
| XGBoost | Runs prediction model |
| Streamlit | Web app deployment |

---

## 📁 Project Structure

```
ipl-player-analyzer/
│
├── app.py                 # Streamlit web application
├── requirements.txt       # Dependencies
├── IPL_Analysis.ipynb     # Complete EDA + ML notebook
└── README.md
```

## 👤 Author
**Yash**
Data Science Enthusiast | B.Tech Student

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](<www.linkedin.com/in/yash-dhollakhandi-94a618337>)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black)](<https://github.com/Yash98911>)
