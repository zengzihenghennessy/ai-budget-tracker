%%writefile app.py
import streamlit as st
from ai_brain import predict_category, predict_goal_date, rebalance_budget
import pandas as pd

st.set_page_config(page_title="AI Savings Tracker", layout="wide")
st.title("AI Budget & Savings Tracker")

# Initialize memory (session state) to store logged expenses
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# --- SIDEBAR: Income & Goal Inputs ---
st.sidebar.header("Your Financial Plan")
weekly_income = st.sidebar.number_input("Weekly Income ($)", min_value=0.0, value=1000.0, step=50.0)
savings_goal = st.sidebar.number_input("Savings Goal ($)", min_value=0.0, value=5000.0, step=100.0)
current_savings = st.sidebar.number_input("Starting Savings ($)", min_value=0.0, value=1200.0, step=100.0)

# --- STEP 1 VISUALS: PROGRESS BAR & METRICS ---
st.subheader("Savings Goal Progress")

# Calculate total spent and remaining savings
total_spent = sum(item["Amount ($)"] for item in st.session_state.expenses)
weekly_saved = max(weekly_income - total_spent, 0.0)
total_saved_now = current_savings + weekly_saved
remaining_goal = max(savings_goal - total_saved_now, 0.0)

# Display 3 metric cards side-by-side
m1, m2, m3 = st.columns(3)
m1.metric("Total Saved So Far", f"${total_saved_now:,.2f}", delta=f"+${weekly_saved:,.2f} this week")
m2.metric("Logged Expenses (This Week)", f"${total_spent:,.2f}")
m3.metric("Remaining to Goal", f"${remaining_goal:,.2f}")

# Progress bar (clamped between 0.0 and 1.0)
progress_ratio = min(total_saved_now / savings_goal, 1.0) if savings_goal > 0 else 0.0
st.progress(progress_ratio, text=f"{int(progress_ratio * 100)}% of your ${savings_goal:,.0f} goal reached")

# --- MAIN AREA: Log an Expense ---
st.divider()
st.subheader("Log a New Expense")
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    desc = st.text_input("Expense Description", placeholder="e.g., Groceries, Coffee, Uber")
with col2:
    amount = st.number_input("Amount ($)", min_value=0.0, value=15.0, step=5.0)
with col3:
    st.write("")
    st.write("")
    log_clicked = st.button("Log Expense", use_container_width=True)

if log_clicked:
    if desc.strip() == "":
        st.warning("Please enter a description before logging.")
    else:
        category, accuracy = predict_category(desc)
        st.session_state.expenses.append({
            "Description": desc,
            "Amount ($)": amount,
            "Category": f"{category} ({accuracy})"
        })
        st.rerun()

# --- DISPLAY LOGGED EXPENSES ---
st.subheader("Recent Expenses")
if len(st.session_state.expenses) > 0:
    df = pd.DataFrame(st.session_state.expenses)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No expenses logged yet. Add one above to see the progress bar update live!")
