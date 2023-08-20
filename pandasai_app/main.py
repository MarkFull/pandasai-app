import streamlit as st
from openai.error import OpenAIError
import sys
import os
sys.path.append(os.path.abspath('.'))

from pandasai_app.components.sidebar import sidebar
from pandasai_app.utils import parse_csv, run_pandasai_openaiapi, clear_submit

if __name__ == '__main__':

    st.set_page_config(
        page_title="PANDASAI APP: Generative AI with Pandas",
        page_icon="📖",
        layout="wide",
        initial_sidebar_state="expanded",)
    st.header("📖 Pandasai App")
    sidebar()

    # Upload the File
    uploaded_files = st.file_uploader(
        "Upload a csv file",
        accept_multiple_files=True,
        type=["csv"],
        help="CSV Files are supported as of now!",
        on_change=clear_submit,
    )

    index = None
    doc = None
    dfs = []

    # for each file uploaded, parse it and add it to the list of dataframes
    for uploaded_file in uploaded_files:
        if uploaded_file is not None:
            if uploaded_file.name.endswith(".csv"):
                df = parse_csv(uploaded_file)
                dfs.append(df)
                index = True
            else:
                raise ValueError("File type not supported!")

    query = st.text_area("Ask a question about the dataframe/csv uploaded", on_change=clear_submit)
    with st.expander("Advanced Options"):
        _verbose = st.checkbox("Show Details About Python Code generated")
        _enforce_privacy = st.checkbox("Enforce Privacy About Personal Data")

    button = st.button("Submit")

    # On SUBMIT of the button
    if button or st.session_state.get("submit"):
        if not st.session_state.get("api_key_configured"):
            st.error("Please configure your OpenAI API key!")
        elif not index:
            st.error("Please upload a data file!")
        elif not query:
            st.error("Please enter a question!")
        else:
            st.session_state["submit"] = True
            # Output Columns
            query_col, answer_col = st.columns(2)
            # sources = search_docs(index, query)
            try:
                answer = run_pandasai_openaiapi(dfs=dfs, prompt=query, verbose=True)

                with query_col:
                    st.markdown("#### Query")
                    st.markdown(query)
                with answer_col:
                    st.markdown("#### Answer")
                    st.markdown(answer)

            except OpenAIError as e:
                st.error(e._message)
