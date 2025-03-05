import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Growth Mindset Tracker", layout="wide")

# Apply styling
st.markdown(
    """
    <style>
    .stApp{
        background-color: black;
        color: white;
        }
        </style>
        """,
    unsafe_allow_html=True
)

# Title and Description
st.title("Datasweeper Sterling Tracker By M. Sameer Awan")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization. Creating the project for quarter 3!")

# Upload data file
uploaded_files = st.file_uploader("Upload your files (accepts CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file, engine="openpyxl")
        else:
            st.error("Unsupported file format. Please upload CSV or Excel files.")
            continue

        # File Preview
        st.write(f"### Preview of {file.name}")
        st.dataframe(df.head())

        # Data Cleaning
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)
            
            if col1.button(f"Remove duplicates from {file.name}"):
                df = df.drop_duplicates()  # Updating df correctly
                st.write("Duplicates removed!")

            if col2.button(f"Handle missing values in {file.name}"):
                numeric_cols = df.select_dtypes(include=['number']).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.write("Missing values handled!")

        # Column Selection
        st.subheader("Select Columns to Keep")
        selected_columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]

        # Data Visualization
        st.subheader("Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # Conversion Options
        st.subheader("Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()

            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)  # Ensure buffer is ready for download

            st.download_button(
                label=f"Download {file_name}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("All files processed successfully!")
