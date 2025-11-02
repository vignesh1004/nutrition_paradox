import streamlit as st

# ----------------------------
# Home Page Content
# ----------------------------
# Read the image as bytes
with open("assets/who_logo.png", "rb") as f:
    logo_bytes = f.read()

# Convert to base64 string (safe for HTML)
import base64
logo_b64 = base64.b64encode(logo_bytes).decode()

# Display logo + title in one line
st.markdown(f"""
    <div style="display: flex; align-items: flex-start; gap: 22px;">
        <img src="data:image/png;base64,{logo_b64}" width="70" style="margin-top: -50px;" />
        <h1 style="font-size: 36px; margin: 0; margin-top: -50px; line-height: 0.5;">
            Nutrition Paradox: A Global View on Obesity and Malnutrition
        </h1>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")
    
st.markdown("""
Welcome to the **Nutrition Paradox Dashboard**.  
This app explores the coexistence of **obesity (overnutrition)** and **malnutrition (undernutrition)** across 200+ countries using **WHO Global Health Observatory data** from 2012–2022.
""")
st.subheader("💡 Key Insights")
st.markdown("""
    - **India & Nigeria** show the nutrition paradox: high malnutrition + rising obesity.
    - **Female obesity (28.6%) > Male (20.7%)**, but malnutrition is nearly equal by gender.
    - **Americas**: High obesity (28.5%), low malnutrition (3.6%).
    - **Africa**: Moderate obesity (10.2%), higher malnutrition (11.2%).
    - **Pacific Islands** (e.g., Nauru, American Samoa) have >68% obesity — world’s highest.
    - **Djibouti, Eritrea** have high CI_Width (>14) → data reliability concerns.
    """)

# Two-column layout
col1, col2 = st.columns(2)

# Column 1: Business Use Cases + Key Insights
with col1:
    st.subheader("📊 Key Features")
    st.markdown("""
    - **25 SQL Queries** with interactive tables and visualizations
    - **Obesity & Malnutrition Trends** (2012–2022)
    - **Country, Region, Gender, and Age Group Filters**
    - **Confidence Interval (CI) Analysis** for data reliability
    - **Combined Insights** revealing the global nutrition paradox
    """)

# Column 2: Key Features + How to Use
with col2:

    st.subheader("🧭 How to Use This App")
    st.markdown("""
    1. Click **“Query Dashboard”** in the sidebar.
    2. Select a category: **Obesity**, **Malnutrition**, or **Combined**.
    3. Choose a query from the dropdown.
    4. View the **data table** and **visualization**.
    5. Use insights to inform health strategy decisions.
    """)
