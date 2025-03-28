import streamlit as st
from tab_concept_load import concept_load_tab
from tab_semantics import semantics_tab

def launch_dashboard():
    tab_column_load, tab_semantics = st.tabs(["Load Concepts", "Semantics"])

    with tab_column_load:
        concept_load_tab()

        with tab_semantics:
            semantics_tab()

    