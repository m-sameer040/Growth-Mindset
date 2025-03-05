import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Growth Mindset Tracker", layout="wide")

# Load data from local CSV file
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
st.title("Datasweeper Sterling Tracker By M.Sameer Awan")
st.write("Transform your files between CSV and Excel formates with built-in data cleaning and visualization Creating the project for quarter 3!")

# Upload data file
uploaded_file = st.file_uploader("Upload your files (accepts CSV or Excel):", type=["cvs","xlsx"], accept_multiple_files=(True))

if uploaded_file:
    for file in uploaded_file:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error("Unsupported file format. Please upload CSV or Excel files.")
            continue

        # File Details
        st.write("Preview the head of the DataFrame")
        st.dataframe(df.head())

        # Data Cleaning
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)
           
            with col1:
                if st.button(f"Remove duplicates from the file : {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates removed!")

            with col2:
                if st.button(f"Handle missing values in the file : {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values handled!")

        st.subheader("Select Coloumns to Keep")
        columns = st.multiselect(f"Choose coloumns for {file.name}",df.columns, default=df.columns)
        df = df[columns]


        # Data Visualization
        st.subheader("Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # Conversion Options 

        st.subheader("Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CVS" , "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data = buffer,
                file_name=file_name,
                mime=mime_type
            )
            
st.success("All files processed successfully!")