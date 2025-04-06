import streamlit as st
import pandas as pd
import itertools
import csv
import io

# Page setup
st.set_page_config(page_title="Part Number Generator", layout="wide")

# Custom styling (light background for inputs + button styling)
st.markdown("""
<style>
textarea {
    background-color: #f2f2f2 !important;
    border-radius: 6px;
}
div.stButton > button {
    background-color: #4B7BEC;
    color: white;
    border: none;
    padding: 0.5em 1em;
    border-radius: 6px;
}
div.stButton:hover > button {
    background-color: #3A5FDB;
}
</style>
""", unsafe_allow_html=True)

# Title & instructions
st.title("Part Number Generator")
st.markdown("""
Enter values for each column below.  
Use **commas** to separate multiple values (e.g., `A,B,C` or `1,2,3`).  
You can input **letters**, **numbers**, or **symbols**.
""")

# Optional prefix input
prefix = st.text_input("Prefix (Optional)", placeholder="Enter prefix like M27500 or leave empty if not needed")

# Session state for column count
if "num_columns" not in st.session_state:
    st.session_state.num_columns = 1

# Status message container
status_placeholder = st.empty()

# Button row
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Add Column"):
        st.session_state.num_columns += 1
        st.toast("✅ Column added!")

with col2:
    if st.session_state.num_columns > 1 and st.button("Remove Column"):
        st.session_state.num_columns -= 1
        st.toast("🗑️ Column removed!")


# Input fields
columns_data = []
for i in range(st.session_state.num_columns):
    input_text = st.text_area(
        f"Column {i + 1}",
        placeholder="Enter values like A,B,C or 1,2,3",
        key=f"col_{i}"
    )
    values = [v.strip() for v in input_text.split(",") if v.strip()]
    columns_data.append(values)

# Generate CSV button
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
