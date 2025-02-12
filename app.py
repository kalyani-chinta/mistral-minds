import streamlit as st
import pandas as pd
import numpy as np
import torch 
import transformers 

# --- Title and Introduction ---
st.title("Ethical Decision-Making Framework")
st.markdown(
    """
    This interactive tool guides you through a structured process to analyze ethical dilemmas. 
    It incorporates key ethical principles and helps you evaluate the potential consequences of different actions.
    """
)

# --- Define Ethical Principles ---
ethical_principles = {
    "Utilitarianism": "Maximize overall happiness and well-being.",
    "Deontology": "Follow universal moral rules and duties.",
    "Virtue Ethics": "Act in accordance with virtuous character traits.",
    "Justice": "Ensure fairness and equitable distribution of resources.",
    "Care Ethics": "Prioritize relationships and responsibilities to others."
}

# --- Define Stakeholders ---
stakeholders = [
    "Individual",
    "Organization",
    "Community",
    "Environment",
    "Other"
]

# --- Define Consequences Impact Type
consequences_impact = [
    "Financial",
    "Social",
    "Environmental",
    "Legal",
    "Reputational",
    "Psychological",
    "Other"
]

# --- Helper Functions ---
def calculate_weighted_score(df, principle_weights):
    """Calculates a weighted score based on principle weights."""
    weighted_scores = []
    for index, row in df.iterrows():
        score = 0
        for principle, weight in principle_weights.items():
            score += row[principle] * weight
        weighted_scores.append(score)
    return weighted_scores


# --- 1. Define the Ethical Dilemma ---
st.header("1. Define the Ethical Dilemma")
dilemma_description = st.text_area("Describe the ethical dilemma you are facing:", height=100)

# --- 2. Identify Stakeholders ---
st.header("2. Identify Stakeholders")
selected_stakeholders = st.multiselect("Identify the stakeholders affected by this dilemma:", stakeholders)
if "Other" in selected_stakeholders:
    other_stakeholder = st.text_input("Specify the 'Other' stakeholder:")
    if other_stakeholder:
        selected_stakeholders.append(other_stakeholder)
        selected_stakeholders.remove("Other")


# --- 3. Brainstorm Possible Actions ---
st.header("3. Brainstorm Possible Actions")
num_actions = st.number_input("How many possible actions are you considering?", min_value=2, max_value=10, value=3, step=1)
actions = []
for i in range(num_actions):
    action = st.text_input(f"Action {i+1}: Describe the action", key=f"action_{i}")
    actions.append(action)

# --- 4. Evaluate Actions Based on Ethical Principles ---
st.header("4. Evaluate Actions Based on Ethical Principles")

# Principle Weights
st.subheader("Assign Weights to Ethical Principles")
principle_weights = {}
for principle in ethical_principles:
    principle_weights[principle] = st.slider(f"Weight for {principle}:", min_value=0.0, max_value=1.0, value=0.2, step=0.05)

# Action Evaluation Table
data = []
for action in actions:
    row = {"Action": action}
    for principle in ethical_principles:
        row[principle] = st.slider(f"Action: {action}, Principle: {principle}", min_value=-5, max_value=5, value=0, step=1, key=f"{action}_{principle}")
    data.append(row)

df = pd.DataFrame(data)
df = df.set_index("Action")

st.dataframe(df)

# --- 5. Analyze Potential Consequences ---
st.header("5. Analyze Potential Consequences")

# Consequences DataFrame
consequences_data = []

for action in actions:
    for stakeholder in selected_stakeholders:
        row = {"Action": action, "Stakeholder": stakeholder}
        for impact in consequences_impact:
            row[impact] = st.slider(f"Action: {action}, Stakeholder: {stakeholder}, Impact: {impact}", min_value=-5, max_value=5, value=0, step=1, key=f"{action}{stakeholder}{impact}")
        consequences_data.append(row)

consequences_df = pd.DataFrame(consequences_data)

if not consequences_df.empty:
    consequences_df = consequences_df.set_index(["Action", "Stakeholder"])
    st.dataframe(consequences_df)

    # --- 6. Make a Decision ---
    st.header("6. Make a Decision")

    # Calculate Weighted Scores
    df['Weighted Score'] = calculate_weighted_score(df, principle_weights)

    # Display Results
    st.subheader("Action Evaluation Results (Based on Ethical Principles)")
    st.dataframe(df)
    best_action = df['Weighted Score'].idxmax()
    st.success(f"Based on the weighted scores, the recommended action is: *{best_action}*")

    # Additional Notes
    st.subheader("Additional Notes and Justification")
    justification = st.text_area("Explain your final decision and its rationale:", height=150)

else:
    st.warning("Please select at least one stakeholder to analyze consequences.")

# --- Display Ethical Principles ---
st.sidebar.header("Ethical Principles Defined")
for principle, definition in ethical_principles.items():
    st.sidebar.subheader(principle)
    st.sidebar.write(definition)
