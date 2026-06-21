import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 1. Page Frame Setup
st.set_page_config(page_title="Bhuvi Wealth Dashboard", layout="wide")
st.title("📊 Bhuvi Wealth Dashboard")
st.caption("Project Sponsor: Sudhanshu Malik | Project Owner: Bhuvi")

# 2. Left Side Dynamic Sliders
st.sidebar.header("👣 Baseline Assumptions")
current_age = st.sidebar.number_input("Current Age", min_value=18, max_value=50, value=18)
target_age = st.sidebar.number_input("Model Until Age", min_value=40, max_value=100, value=60)
years_to_model = target_age - current_age

st.sidebar.header("💰 Income & Savings")
starting_salary_monthly = st.sidebar.number_input("Expected Starting Monthly Income ($)", value=3000)
annual_salary_growth = st.sidebar.slider("Annual Salary Growth (%)", 0.0, 15.0, 5.0) / 100

st.sidebar.header("📈 Investment Parameters")
initial_investment = st.sidebar.number_input("Initial Investment ($)", value=1000)
expected_return = st.sidebar.slider("Expected Annual Return (%)", 4.0, 12.0, 8.0) / 100

# 3. Behind-the-Scenes Math Calculator
def run_simulation(monthly_save_amount):
    ages, net_worth_history, total_contributions = [], [], []
    current_net_worth = initial_investment
    cumulative_contributions = initial_investment
    current_monthly_salary = starting_salary_monthly
    
    for year in range(years_to_model):
        ages.append(current_age + year)
        for month in range(12):
            actual_save = min(monthly_save_amount, current_monthly_salary)
            current_net_worth = current_net_worth * (1 + expected_return / 12) + actual_save
            cumulative_contributions += actual_save
            
        net_worth_history.append(round(current_net_worth, 2))
        total_contributions.append(round(cumulative_contributions, 2))
        current_monthly_salary *= (1 + annual_salary_growth)
        
    return ages, net_worth_history, total_contributions

# 4. Creating the Interactive Tabs
tabs = st.tabs(["⏳ The Cost of Waiting", "📊 Savings Power", "⚖️ Earning vs Spending"])

# --- TAB 1: THE COST OF WAITING (Q1) ---
with tabs[0]:
    st.subheader("The Cost of Delaying: Investing at 18 vs 25")
    monthly_test_save = st.slider("Test Monthly Savings Amount ($)", 100, 2000, 500)
    
    ages_early, nw_early, _ = run_simulation(monthly_test_save)
    
    # Late Starter Math Loop
    nw_late = []
    current_late_nw = initial_investment
    for year in range(years_to_model):
        age = current_age + year
        if age < 25:
            nw_late.append(initial_investment)
        else:
            for month in range(12):
                current_late_nw = current_late_nw * (1 + expected_return / 12) + monthly_test_save
            nw_late.append(round(current_late_nw, 2))

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=ages_early, y=nw_early, name="Starts Investing at Age 18", line=dict(color='green', width=3)))
    fig2.add_trace(go.Scatter(x=ages_early, y=nw_late, name="Starts Investing at Age 25", line=dict(color='crimson', width=3)))
    fig2.update_layout(xaxis_title="Age", yaxis_title="Projected Wealth ($)", template="plotly_white")
    st.plotly_chart(fig2, use_container_width=True)
    
    gap = nw_early[-1] - nw_late[-1]
    st.warning(f"Waiting 7 years until age 25 completely costs you **${gap:,.2f}** by the time you turn {target_age}!")

# --- TAB 2: SAVINGS POWER (Q2) ---
with tabs[1]:
    st.subheader("The Compounding Impact of Extra Monthly Savings")
    ages, nw_base, _ = run_simulation(200)
    _, nw_plus_100, _ = run_simulation(200 + 100)
    _, nw_plus_500, _ = run_simulation(200 + 500)
    _, nw_plus_1k, _ = run_simulation(200 + 1000)
    
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=ages, y=nw_base, name="Base Savings ($200/mo)"))
    fig1.add_trace(go.Scatter(x=ages, y=nw_plus_100, name="Base + $100/mo", line=dict(dash='dash')))
    fig1.add_trace(go.Scatter(x=ages, y=nw_plus_500, name="Base + $500/mo", line=dict(dash='dot')))
    fig1.add_trace(go.Scatter(x=ages, y=nw_plus_1k, name="Base + $1,000/mo", line=dict(width=3, color='green')))
    fig1.update_layout(xaxis_title="Age", yaxis_title="Projected Wealth ($)", template="plotly_white")
    st.plotly_chart(fig1, use_container_width=True)

# --- TAB 3: EARNING VS SPENDING (Q3) ---
with tabs[2]:
    st.subheader("High Income / High Spender vs. Moderate Income / Disciplined Saver")
    _, nw_high_earner, _ = run_simulation(900)   # High income, low relative savings
    _, nw_high_saver, _ = run_simulation(1400)   # Moderate income, aggressive savings rate
    
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=ages_early, y=nw_high_earner, name="High Income / High Burn Rate (Saves $900/mo)", line=dict(color='orange')))
    fig3.add_trace(go.Scatter(x=ages_early, y=nw_high_saver, name="Moderate Income / High Savings Rate (Saves $1,400/mo)", line=dict(color='teal', width=3)))
    fig3.update_layout(xaxis_title="Age", yaxis_title="Projected Wealth ($)", template="plotly_white")
    st.plotly_chart(fig3, use_container_width=True)
