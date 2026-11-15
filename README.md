# ai-budget-tracker
AI Budget & Savings Tracker: Teen Allowance Optimizer
Team: Julien (Chayapol Luanan) & Ziheng (Hennes) Zeng (Year 10) | Event: Veritas AI Finance Hackathon
Tech Stack: Python, Pandas, Scikit-learn, Streamlit, GitHub

1. Problem Statement
Most budgeting apps are designed for adults managing fixed monthly paychecks and utility bills. Teenagers handle irregular income from allowances or part-time jobs alongside frequent, small social purchases like bubble tea and concert tickets. Because manual expense tracking is tedious, students quickly abandon standard budgeting tools. We built an automated web app that classifies daily teen expenses from plain text and adjusts weekly spending targets whenever an impulse purchase threatens a savings goal.

2. Dataset & Methodology
We created a synthetic dataset (teen_finances.csv) of 180 teen transactions labeled as Needs, Wants, or Income. Our Streamlit app (app.py) connects to an AI backend (ai_brain.py) with two core models:
- Hybrid Expense Classifier: Combines a TF-IDF vectorizer and Logistic Regression with teen keyword rules to categorize informal purchase descriptions automatically.
- Goal Forecaster & Rebalancer: Uses Linear Regression to project the exact goal completion date and calculates how much to trim from upcoming weekly "Wants" budgets after an overspend.

3. Results & Limitations
Accuracy Gain: Adding teen keyword rules to our baseline TF-IDF + Logistic Regression model boosted classification accuracy from 75% to 90%.
Limitations & Future Work: Because the model uses 180 synthetic examples, unfamiliar local store names can occasionally be misclassified. Future updates will add user label corrections and CSV imports from teen debit cards.

**2-Minute Demo Video:** [Watch the Live Demo](https://youtu.be/Oe5qiOS6L7M)

