import streamlit as st
from datetime import datetime
import pandas as pd

# Page title
st.title("NORAM QA Validation Tool")

# Agent Details
agent_name = st.text_input("Agent Name")

ticket_number = st.text_input("Ticket Number")

airline = st.selectbox(
    "Airline",
    ["AA", "UA", "DL", "BA"]
)

original_fare = st.number_input(
    "Original Fare",
    min_value=0.0
)

new_fare = st.number_input(
    "New Fare",
    min_value=0.0
)

penalty = st.number_input(
    "Penalty",
    min_value=0.0
)

fop = st.selectbox(
    "Form of Payment",
    ["Credit Card", "Cash", "Voucher", "MCO"]
)

ticket_validity = st.date_input(
    "Ticket Validity Date"
)

cancellation_done = st.selectbox(
    "Cancellation Done?",
    ["Yes", "No"]
)

# import pandas as pd

# Validation button
if st.button("Validate Case"):

    errors = []

    today = datetime.today().date()

    # Rule 1
    if ticket_validity < today:
        errors.append("Expired ticket")

    # Rule 2
    if cancellation_done == "No":
        errors.append("Cancellation not completed")

    # Rule 3
    if penalty == 0:
        errors.append("Penalty missing")

    # Rule 4
    if fop == "MCO":
        errors.append("Supervisor approval needed")

    # Final Result
    if len(errors) == 0:
        result = "SAFE"

        st.success("SAFE TO PROCESS")

    else:
        result = "ALERT"

        st.error("VALIDATION ALERT")

        for error in errors:
            st.write("- " + error)

    # -----------------------------
    # SAVE LOGS
    # -----------------------------

    data = {
        "Agent": [agent_name],
        "Ticket": [ticket_number],
        "Airline": [airline],
        "Original Fare": [original_fare],
        "New Fare": [new_fare],
        "Penalty": [penalty],
        "FOP": [fop],
        "Validity Date": [ticket_validity],
        "Cancellation": [cancellation_done],
        "Errors": [", ".join(errors)],
        "Result": [result]
    }

    df = pd.DataFrame(data)

    try:
        old_df = pd.read_csv("validation_logs.csv")
        df = pd.concat([old_df, df], ignore_index=True)

    except:
        pass

    df.to_csv("validation_logs.csv", index=False)

    st.info("Case logged successfully")