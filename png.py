import streamlit as st
import pandas as pd
import itertools
import io
import csv

st.set_page_config(page_title="Generate Part Numbers", layout="wide")

st.title("🔢 Generate Part Numbers")
st.write("Add values separated by commas in each column. You can enter letters, numbers, or symbols.")

# 🔹 Optional prefix
prefix = st.text_input("Prefix (Optional)", placeholder="e.g., M27500-")

# 🔹 Session state to track number of columns
if "num_columns" not in st.session_state:
    st.session_state.num_columns = 1

# 🔹 Add Column button
if st.button("➕ Add Column"):
    st.session_state.num_columns += 1

# 🔹 Create text areas for each column
columns_data = []
for i in range(st.session_state.num_columns):
    user_input = st.text_area(
        f"Column {i + 1}",
        placeholder="Add values separated by commas (e.g., A,B,C or 1,2,3)",
        key=f"col_{i}"
    )
    columns_data.append(user_input)

# 🔹 Generate CSV using original logic
if st.button("🚀 Generate CSV"):
    try:
        # Convert inputs to lists
        cols = [col.strip().split(",") for col in columns_data if col.strip()]

        # Generate combinations
        combinations = itertools.product(*cols)

        # Create in-memory CSV
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Part Number"])
        for combo in combinations:
            writer.writerow([prefix + ''.join(combo)])

        # Download button
        st.download_button(
            label="📥 Download CSV",
            data=output.getvalue(),
            file_name="part_numbers.csv",
            mime="text/csv"
        )

        st.success(f"CSV generated successfully with {len(list(itertools.product(*cols)))} part numbers!")

    except Exception as e:
        st.error(f"An error occurred: {e}")
