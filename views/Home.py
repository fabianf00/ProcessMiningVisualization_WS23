from views.ViewInterface import ViewInterface
import streamlit as st
import os
from utils.transformations import dataframe_to_cases_list
from utils.io import read_file, supported_formats


class Home(ViewInterface):
    def render(self):
        st.title("Welcome to the Process Mining Tool")
        st.write(
            "This tool is designed to help you visualize the dependencies between activities in your process logs."
        )
        st.write("To get started, upload a CSV file containing your process logs.")

        file = st.file_uploader(
            "Upload a file",
            type=["csv", *supported_formats],
            accept_multiple_files=False,
        )

        if file:
            df = read_file(file)
            st.session_state.df = df
            st.session_state.page = "ColumnSelectionView"
            st.rerun()