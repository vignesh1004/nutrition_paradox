import streamlit as st

# Main page configuration
st.set_page_config(
    page_title = "Nutrition Paradox Dashboard",
    page_icon = "assets/who_logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Apply global CSS for WHO-style font
st.markdown("""
    <style>
    body {
        font-family: Frutiger Bold Condensed, 'Segoe UI',  Tahoma, Geneva, Verdana, sans-serif;
        color: #0072BB ;
    }
    h1, h2, h3 {
        color: #009EDB  !important;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# Navigation Setup
# ----------------------------
# Define pages as a list of st.Page objects
home_page = st.Page("pages/home.py", title="🏠 Home")
queries_page = st.Page("pages/queries.py", title="📊 Query Dashboard")

# Create navigation
pg = st.navigation([home_page, queries_page])
# Run the selected page
pg.run()