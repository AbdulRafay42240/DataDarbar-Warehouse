import streamlit as st
import pandas as pd
import os

# Set up the Streamlit page
st.set_page_config(page_title="Data Darbar Dataset Warehouse", page_icon=":bar_chart:")

# Add a top heading with logo placeholder and style the page
st.markdown("""
    <style>
        .stButton>button {
            background-color: #ffffff;  /* White button background */
            color: #000000;  /* Black button text color */
            border: 2px solid #000000;  /* Black border */
            padding: 10px 20px;  /* Padding */
            font-size: 16px;  /* Font size */
            font-weight: bold;  /* Bold text */
            border-radius: 5px;  /* Rounded corners */
        }
        .stButton>button:hover {
            background-color: #f0f0f0;  /* Light grey background on hover */
            color: #000000;  /* Black text color on hover */
        }
    </style>
""", unsafe_allow_html=True)

# Add a top heading and logo image
st.markdown("<div class='header'><h1>Data Darbar Dataset Warehouse</h1></div>", unsafe_allow_html=True)
# st.image("data_darbar_logo.jpeg", use_column_width=True)  # Adjust the path if necessary
st.image("data_darbar_logo.jpeg", width=100)  # Adjust the width as needed


# Directory containing your data files
folder_path = '.'

# Get the list of files in the folder
files = [f for f in os.listdir(folder_path) if f.endswith('.csv') or f.endswith('.xlsx')]

if not files:
    st.write("No data files found in the directory.")
else:
    # Allow user to select multiple files
    selected_files = st.multiselect("Select one or more data files", files)

    if selected_files:
        dataframes = []
        for i, file in enumerate(selected_files):
            # Determine file extension and load accordingly
            file_path = os.path.join(folder_path, file)
            if file.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            
            # Rename columns to avoid conflicts by appending a unique suffix
            df.columns = [f"{col}_{i}" for col in df.columns]
            
            # Add the DataFrame to the list
            dataframes.append(df)
        
        # Merge the dataframes column-wise
        try:
            merged_data = pd.concat(dataframes, axis=1)
            
            # Display the merged data
            st.dataframe(merged_data)
        
        except Exception as e:
            st.write(f"Error during merging: {e}")

        # Create a function to download the merged dataset as an Excel file
        def download_link(data):
            # Convert DataFrame to Excel
            import io
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                data.to_excel(writer, index=False, sheet_name='MergedData')
            return output.getvalue()

        # Provide a download button for the merged dataset
        st.download_button(
            label="Download Merged Dataset as Excel",
            data=download_link(merged_data),
            file_name='merged_dataset.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
