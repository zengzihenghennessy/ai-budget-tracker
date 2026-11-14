import streamlit as st
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

# --- MAIN AREA: Log an Expense ---
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
        st.session_state.expenses.append({
            "Description": desc,
            "Amount ($)": amount,
            "Category": "Uncategorized (Placeholder)"
        })
        st.success(f"Logged '{desc}' for ${amount:.2f}")

# --- DISPLAY LOGGED EXPENSES ---
st.divider()
st.subheader("Recent Expenses")
if len(st.session_state.expenses) > 0:
    df = pd.DataFrame(st.session_state.expenses)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No expenses logged yet. Add one above to test the layout!")
