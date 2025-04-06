import streamlit as st
import pandas as pd
import itertools
import csv
import io

# Configure the page
st.set_page_config(page_title="Part Number Generator", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        body {
            background-color: #f9f9f9;
        }
        .stTextInput > div > div > input {
            background-color: #ffffff;
            border-radius: 8px;
        }
        .stTextArea textarea {
            background-color: #ffffff;
            border-radius: 8px;
        }
        .stButton button {
            border-radius: 6px;
            background-color: #005A9C;
            color: white;
            font-weight: 500;
        }
        .stButton button:hover {
            background-color: #004377;
        }
        .stDownloadButton button {
            border-radius: 6px;
            background-color: #007F5F;
            color: white;
            font-weight: 500;
        }
        .stDownloadButton button:hover {
            background-color: #00684a;
        }
    </style>
""", unsafe_allow_html=True)

# Page title and instructions
st.title("Part Number Generator")
st.markdown("Generate all combinations of product part numbers by entering possible values in each column.")

# Prefix input
prefix = st.text_input("Prefix (Optional)", "M27500")

st.markdown("#### Enter values for each column")
st.markdown("Use commas to separate values in each field. You can input letters, numbers, or symbols.")

# Manage dynamic column count in session
if "num_columns" not in st.session_state:
    st.session_state.num_columns = 1

# Buttons to add/remove columns
control_cols = st.columns([1, 1, 6])
with control_cols[0]:
    if st.button("Add Column"):
        st.session_state.num_columns += 1
with control_cols[1]:
    if st.session_state.num_columns > 1 and st.button("Remove Column"):
        st.session_state.num_columns -= 1

# Text input areas for columns
columns_data = []
input_cols = st.columns(st.session_state.num_columns)

for i in range(st.session_state.num_columns):
    with input_cols[i]:
        input_text = st.text_area(
            f"Column {i + 1}",
            placeholder="e.g., A,B,C or 1,2,3",
            key=f"col_{i}"
        )
        values = [v.strip() for v in input_text.split(",") if v.strip()]
        columns_data.append(values)

# Generate button and CSV logic
if st.button("Generate CSV"):
    try:
        if all(columns_data) and all(len(col) > 0 for col in columns_data):
            combinations = itertools.product(*columns_data)

            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["Part Number"])
            for combo in combinations:
                writer.writerow([prefix + ''.join(combo)])

            csv_data = output.getvalue().encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name="part_numbers.csv",
                mime="text/csv"
            )

            st.success(f"Successfully generated {len(list(itertools.product(*columns_data)))} part numbers.")
        else:
            st.warning("Please ensure all columns contain at least one value.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
