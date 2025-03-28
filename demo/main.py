import streamlit as st
from dashboard import launch_dashboard

st.set_page_config(
    layout = 'wide',
    page_title = 'semantical',
    initial_sidebar_state = "auto"
)

st.title('Semantical')

with st.sidebar:
    st.write(
        """
        SEMANTICAL\n
        """
    )

launch_dashboard()