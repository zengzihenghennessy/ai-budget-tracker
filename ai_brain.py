import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score

# 1. Load data safely (works regardless of which folder Streamlit runs from)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "teen_finances.csv")

df = pd.read_csv(CSV_PATH)
expenses_df = df[df["category"].isin(["Needs", "Wants"])]

X = expenses_df["description"]
y = expenses_df["category"]

# 2. Split and train the ML Pipeline
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

model = make_pipeline(
    TfidfVectorizer(ngram_range=(1, 2), stop_words="english"),
    LogisticRegression()
)
model.fit(X_train, y_train)

# 3. Hybrid Classifier (Domain Keywords + Machine Learning)
def classify_expense(text):
    clean_text = str(text).strip().lower()
    
    obvious_wants = [
        "bubble tea", "boba", "milk tea", "frappuccino", "starbucks", "mcdonalds",
        "gaming", "robux", "v-bucks", "valorant", "concert", "movie", "hoodie",
        "sneakers", "latte", "spotify", "netflix", "manga", "cinema", "pizza",
        "sushi", "donut", "arcade"
    ]
    obvious_needs = [
        "bus", "metro", "subway", "train", "textbook", "notebook", "lunch",
        "cafeteria", "pharmacy", "prescription", "toothpaste", "shampoo",
        "deodorant", "calculator", "charger", "goggles", "groceries", "socks",
        "umbrella", "ink", "study guide"
    ]
    
    if any(word in clean_text for word in obvious_wants):
        return "Wants"
    if any(word in clean_text for word in obvious_needs):
        return "Needs"
        
    return model.predict([clean_text])[0]

# Calculate Hybrid Accuracy Score
hybrid_preds = [classify_expense(item) for item in X_test]
hybrid_accuracy = round(accuracy_score(y_test, hybrid_preds) * 100, 1)

# --- REQUIRED FUNCTIONS FOR STREAMLIT APP ---

def predict_category(text):
    return classify_expense(text), f"{hybrid_accuracy}%"

def predict_goal_date(weekly_savings, target_amount, current_saved=0):
    if weekly_savings <= 0:
        return "Increase weekly savings above $0 to reach your goal."
    if current_saved >= target_amount:
        return "Goal already reached!"

    weeks = np.array([0, 1, 2, 3, 4, 5, 6, 7]).reshape(-1, 1)
    fluctuations = np.array([0, 0.95, 2.05, 2.90, 4.10, 4.95, 6.05, 7.00])
    cumulative_savings = current_saved + (fluctuations * weekly_savings)

    reg = LinearRegression()
    reg.fit(weeks, cumulative_savings)

    slope = reg.coef_[0]
    intercept = reg.intercept_

    weeks_needed = (target_amount - intercept) / slope
    days_needed = int(np.ceil(weeks_needed * 7))

    goal_date = datetime.now() + timedelta(days=days_needed)
    return {
        "weeks_needed": round(weeks_needed, 1),
        "estimated_date": goal_date.strftime("%B %d, %Y")
    }

def rebalance_budget(overspent_amount, weeks_left):
    if overspent_amount <= 0:
        return "You are on budget! No cuts needed."
    if weeks_left <= 0:
        return f"No weeks left in this cycle—roll ${overspent_amount:.2f} over to next month's budget."

    weekly_trim = overspent_amount / weeks_left
    return {
        "weekly_wants_trim": round(weekly_trim, 2),
        "advice": f"Cut ${weekly_trim:.2f} per week from 'Wants' over the next {weeks_left} week(s)."
    }

# Only runs if you test ai_brain.py directly (won't clutter Streamlit)
if __name__ == "__main__":
    print(predict_category("bubble tea after school"))
    print(predict_goal_date(25, 300))
    print(rebalance_budget(45, 3))
