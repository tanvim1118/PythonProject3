import streamlit as st
import pandas as pd
import io

# Set the page title
st.set_page_config(page_title="Excel Merger Bot", page_icon="🤖")

st.title("Excel Merger Bot 🤖")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi there! Upload your Excel files below, and I'll merge them into one single file for you."}
    ]

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# File uploader widget
uploaded_files = st.file_uploader("Upload Excel files here", type=["xlsx", "xls"], accept_multiple_files=True)

# Logic to handle the uploaded files
if uploaded_files:
    # Only trigger if exactly 3 files are uploaded (or you can remove the len check to allow any amount)
    with st.chat_message("user"):
        st.markdown(f"I have uploaded {len(uploaded_files)} files.")

    with st.chat_message("assistant"):
        if len(uploaded_files) < 2:
            st.warning("Please upload at least 2 files to merge them.")
        else:
            st.markdown("Processing and merging your files now...")

            try:
                # 1. Read all uploaded files into a list of DataFrames
                dataframes = [pd.read_excel(file) for file in uploaded_files]

                # 2. Combine them all together
                merged_df = pd.concat(dataframes, ignore_index=True)

                # 3. Convert the merged DataFrame back to an Excel file in memory
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    merged_df.to_excel(writer, index=False, sheet_name='Merged_Data')

                processed_data = output.getvalue()

                st.success("Success! I've merged the files. You can download the result below.")

                # 4. Provide the download button
                st.download_button(
                    label="📥 Download Merged Excel",
                    data=processed_data,
                    file_name="merged_output.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except Exception as e:
                st.error(f"An error occurred while merging: {e}. Please ensure all files have the same structure.")