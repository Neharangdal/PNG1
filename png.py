import streamlit as st
import csv
import itertools
import io

st.set_page_config(page_title="Custom Part Number Generator", layout="centered")
st.title("🔢 Custom Part Number Generator")

# New input for prefix
prefix = st.text_input("Enter Part Number Prefix (e.g. M27500)", "M27500")

st.markdown("Enter comma-separated values for each column below:")

# Input boxes for each column
col1 = st.text_area("Column 1 (e.g. -,A,B,...)", "-,A,B,C,D,E,F,G,H,J,K,L,M,N,P,R,S,T,U,V")
col2 = st.text_area("Column 2 (e.g. 26,24,...)", "26,24,22,20,18,16,14,12,10,8,6,4,2,1,01,02,03,04")
col3 = st.text_area("Column 3 (e.g. WB,WC,...)", "WB,WC,WE,WF,WG,WH,WJ,WK,WL,WM,WN,WP,WR")
col4 = st.text_area("Column 4 (e.g. 1,2,...)", "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15")
col5 = st.text_area("Column 5 (e.g. A,B,...)", "A,B,C,D,E,F,G,H,I,J,K,L,M,N,P,Q,R,S,T,U,V,W,X,Y,Z,HD,HS,ND,NF")
col6 = st.text_area("Column 6 (e.g. 00,06,...)", "00,06,07,11,12,24,56,61,62,74")

if st.button("🚀 Generate CSV"):
    try:
        # Convert inputs to lists
        cols = [c.strip().split(",") for c in [col1, col2, col3, col4, col5, col6]]

        # Generate combinations
        combinations = itertools.product(*cols)

        # Create in-memory CSV
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Part Number"])
        for combo in combinations:
            writer.writerow([prefix + ''.join(combo)])

        # Download button
        st.success("✅ CSV file generated successfully!")
        st.download_button(
            label="📥 Download CSV",
            data=output.getvalue(),
            file_name="part_number_combinations.csv",
            mime="text/csv"
        )
    except Exception as e:
        st.error(f"⚠️ Error: {e}")
