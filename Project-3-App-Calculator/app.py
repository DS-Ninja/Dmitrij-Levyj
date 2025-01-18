import streamlit as st
from datetime import datetime
import pdfplumber
import re


# Function to calculate total days on board
def calculate_days_on_board(date_ranges):
    total_days = 0
    breakdown = []
    for start_date, end_date in date_ranges:
        start = datetime.strptime(start_date, "%d.%m.%Y")
        end = datetime.strptime(end_date, "%d.%m.%Y")
        days = (end - start).days + 1
        total_days += days
        breakdown.append(f"Range: {start_date} to {end_date}, Days: {days}")
    return total_days, breakdown


# Function to calculate total earned free days
def calculate_total_earned_free_days(text_data):
    monthly_totals = []
    for page_text in text_data:
        earned_free_days = 0  # Initialize with default value
        vacation_days = 0  # Initialize with default value
        for line in page_text.splitlines():
            if "1011 Earned free days this month" in line:
                earned_match = re.search(r"1011.*?([-]?\d+,\d+)\s+Days", line)
                if earned_match:
                    earned_free_days = float(earned_match.group(1).replace(",", "."))
            if "1030 Earned vacationdays this month" in line:
                vacation_match = re.search(r"1030.*?([-]?\d+,\d+)\s+Days", line)
                if vacation_match:
                    vacation_days = float(vacation_match.group(1).replace(",", "."))
        monthly_total = earned_free_days + vacation_days
        monthly_totals.append(monthly_total)
    return sum(monthly_totals)


# Streamlit Interface
st.title("Uni-Tankers Calculator by Dimi")

# Input On-Board Dates
st.header("Input On-Board Dates")
num_ranges = st.number_input("How many on-board date ranges?", min_value=1, max_value=12, value=1)
date_ranges = []

for i in range(num_ranges):
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.text_input(f"Start Date (Range {i+1})", placeholder="DD.MM.YYYY")
    with col2:
        end_date = st.text_input(f"End Date (Range {i+1})", placeholder="DD.MM.YYYY")
    if start_date and end_date:
        date_ranges.append((start_date, end_date))

# Upload PDF File for Earned Free Days
st.header("Upload PDF File (Of All 12-Month PaySlips)")
uploaded_file = st.file_uploader("Upload your PDF file", type="pdf")

if st.button("Calculate"):
    # Calculate Total Days on Board
    if date_ranges:
        total_days_on_board, breakdown_on_board = calculate_days_on_board(date_ranges)

    # Calculate Total Earned Free Days
    if uploaded_file:
        with pdfplumber.open(uploaded_file) as pdf:
            text_data = [page.extract_text() for page in pdf.pages]
        total_earned_free_days = calculate_total_earned_free_days(text_data)

    # Calculate Total Days Earned or Settled for Company
    if date_ranges and uploaded_file:
        total_days_earned_or_settled = total_days_on_board - total_earned_free_days

        # Final Results
        st.subheader("1. Final Results")
        st.write(f"**Total Days on Board (calculated):** {total_days_on_board}")
        st.write(f"**Total Earned Free Days:** {total_earned_free_days}")
        st.write(f"**Total Days Earned or Settled for Company:** {total_days_earned_or_settled}")

        # Total Days on Board Calculation
        st.subheader("2. Total Days on Board Calculation")
        st.write(f"**Total Days on Board (calculated):** {total_days_on_board}")
        st.write("**Breakdown of Ranges:**")
        for b in breakdown_on_board:
            st.write(b)

        # Total Earned Free Days Calculation (Compact)
        st.subheader("3. Total Earned Free Days Calculation")
        st.write(f"**Total Earned Free Days (Yearly):** {total_earned_free_days}")
