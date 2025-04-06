import streamlit as st
import pandas as pd
import itertools
import csv
import io

# Page setup
st.set_page_config(page_title="Part Number Generator", layout="wide")

# Custom styling
st.markdown("""
    <style>
    .stTextInput > div > div > input,
    .stTextArea > div > textarea {
        background-color: white !important;
        color: black !important;
        border: 1.5px solid black;
        border-radius: 8px;
        padding: 10px;
        box-shadow: none !important;
    }

    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > textarea::placeholder {
        color: #444 !important;
        font-style: italic;
    }


    div.stButton > button {
        background-color: #2C3E50;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6em 1.5em;
        font-weight: 500;
        transition: 0.3s ease;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
    }

    div.stButton > button:hover {
        background-color: #1A252F;
        color: white;
    }

    div.stButton > button:focus {
        background-color: #2C3E50 !important;
        color: white !important;
        box-shadow: none;
    }

    .stTextArea {
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Title & Instructions
st.title("Part Number Generator")
st.markdown("""
Enter values for each column below.  
Use **commas** to separate multiple values (e.g., A,B,C or 1,2,3).  
You can input **letters**, **numbers**, or **symbols**.
""")

# Prefix input
prefix = st.text_input("Prefix (Optional)", placeholder="Enter prefix like M27500 or leave empty if not needed")

# Session state setup
if "num_columns" not in st.session_state:
    st.session_state.num_columns = 1

# Add/Remove column buttons side-by-side
col1, col2, _ = st.columns([1, 1, 8])
with col1:
    if st.button("➕ Add Column"):
        st.session_state.num_columns += 1
        st.toast("Column added ✅")

with col2:
    if st.session_state.num_columns > 1:
        if st.button("➖ Remove Column"):
            st.session_state.num_columns -= 1
            st.toast("Column removed ⚠️")

# Input Columns
columns_data = []
for i in range(st.session_state.num_columns):
    input_text = st.text_area(
        f"Column {i + 1}",
        placeholder="Enter values like A,B,C or 1,2,3",
        key=f"col_{i}"
    )
    values = [v.strip() for v in input_text.split(",") if v.strip()]
    columns_data.append(values)

# Generate CSV
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

            st.success(f"✅ Successfully generated {len(list(itertools.product(*columns_data)))} part numbers.")
        else:
            st.warning("⚠️ Please fill out all columns with at least one value.")
    except Exception as e:
        st.error(f"❌ Error: {e}")
