
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from database.db import run_query

# ----------------------------
# Title
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
            Nutrition Paradox: Query Dashboard
        </h1>
    </div>
""", unsafe_allow_html=True)


# ----------------------------
# 1. Top-Level Category Buttons
# ----------------------------
st.markdown("### Choose a Category")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🟥 Obesity Data", key="obesity_btn"):
        st.session_state.category = "Obesity"

with col2:
    if st.button("🟦 Malnutrition Data", key="malnutrition_btn"):
        st.session_state.category = "Malnutrition"

with col3:
    if st.button("🟨 Combined Data", key="combined_btn"):
        st.session_state.category = "Combined"

# ----------------------------
# 2. Dynamic Query Selector
# ----------------------------
if 'category' not in st.session_state:
    st.session_state.category = None

if st.session_state.category:
    st.markdown(f"### {st.session_state.category} Queries")

    # Define queries per category
    if st.session_state.category == "Obesity":
        query_options = [
            "Select a query...",
            "1. Top 5 WHO Regions by Average Obesity (2022)",
            "2. Top 5 Countries with Highest Obesity (2022)",
            "3. Obesity trend in India over the years",
            "4. Average obesity by gender",
            "5. Country count by obesity level category and age group",
            "6. Top 5 countries - least reliable & Most consistent",
            "7. Average obesity by age group",
            "8. Top 10 Countries with consistent low obesity",
            "9. Countries where female obesity exceeds male by large margin (same year)",
            "10. Global average obesity percentage per year"
        ]
    elif st.session_state.category == "Malnutrition":
        query_options = [
            "Select a query...",
            "1. Avg. malnutrition by age group",
            "2. Top 5 countries with highest malnutrition (mean_estimate)",
            "3. Malnutrition trend in African region over the years",
            "4. Gender-based average malnutrition",
            "5. Malnutrition level-wise (average CI_Width by age group)",
            "6. Yearly malnutrition change in specific countries (India, Nigeria, Brazil)",
            "7. Regions with lowest malnutrition averages",
            "8. Countries with increasing malnutrition",
            "9. Min/Max malnutrition levels year-wise comparison",
            "10. High CI_Width flags for monitoring (CI_width > 5)"
        ]
    else:  # Combined
        query_options = [
            "Select a query...",
            "1. Obesity vs malnutrition comparison by country (any 5 countries)",
            "2. Gender-based disparity in both obesity and malnutrition",
            "3. Region-wise avg estimates side-by-side (Africa and America)",
            "4. Countries with obesity up & malnutrition down",
            "5. Age-wise trend analysis"
        ]

    selected_query = st.selectbox("Choose a query", query_options, key=f"{st.session_state.category}_query")

    # ----------------------------
    # 3. Run Selected Query
    # ----------------------------
    if selected_query != "Select a query...":
        
        # Add your query logic here (we'll fill them in next)
        if st.session_state.category == "Obesity":

            # ----------------------------
            # Run Selected Query
            # ----------------------------
            if selected_query == "1. Top 5 WHO Regions by Average Obesity (2022)":
                st.subheader("Top 5 regions with the highest average obesity levels in the most recent year(2022)")
                
                query1= """
                    SELECT Region, AVG(Mean_Estimate) AS Avg_Obesity
                    FROM obesity
                    WHERE Year = 2022 AND Region IS NOT NULL
                    GROUP BY Region
                    ORDER BY Avg_Obesity DESC
                    LIMIT 5;
                """
                df1 = run_query(query1)
                st.dataframe(df1, use_container_width=True, height=215)

                # Add visualization
                fig, ax = plt.subplots(figsize=(8, 4))
                bars = ax.barh(df1['Region'], df1['Avg_Obesity'], color='steelblue')
                ax.set_xlabel('Average Obesity (%)')
                ax.set_title('Top 5 Regions by Obesity (2022)')
                ax.grid(axis='x', alpha=0.3)
                for bar in bars:
                    width = bar.get_width()
                    ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, f'{width:.1f}%', 
                            va='center', ha='left', fontsize=9)
                st.pyplot(fig)
                
            elif selected_query == "2. Top 5 Countries with Highest Obesity (2022)":
                st.subheader("Top 5 Countries with Highest Obesity (2022)")
                query2 = """
                    SELECT Country, Mean_Estimate
                    FROM obesity
                    WHERE Year = 2022
                    AND Gender = 'Both'
                    AND age_group = 'Adult'
                    AND Region IS NOT NULL
                    ORDER BY Mean_Estimate DESC
                    LIMIT 5;
                """
                df2 = run_query(query2)
                
                if not df2.empty:
                    st.table(df2)
                else:
                    st.write("No data found.")

            elif selected_query == "3. Obesity trend in India over the years":
                st.subheader("Obesity trend in India over the years(Mean_estimate)")
                query3 = """
                    SELECT Year, Mean_Estimate
                    FROM obesity
                    WHERE Country = 'India' AND Gender = 'Both' AND age_group = 'Adult'
                    ORDER BY Year; 
                """
                df3 = run_query(query3)
                if not df3.empty:
                    st.table(df3)
                    
                    # Visualization: Line chart
                    fig, ax = plt.subplots(figsize=(8, 4))
                    ax.plot(df3['Year'], df3['Mean_Estimate'], marker='o', color='steelblue')
                    ax.set_xlabel('Year')
                    ax.set_ylabel('Obesity (%)')
                    ax.set_title('Obesity Trend in India (2012–2022)')
                    ax.grid(alpha=0.3)
                    for i, row in df3.iterrows():
                        ax.text(row['Year'], row['Mean_Estimate'] + 0.1, f"{row['Mean_Estimate']:.1f}%", 
                                ha='center', va='bottom', fontsize=8)
                    st.pyplot(fig)
                else:
                    st.write("No data found for India.")

            elif selected_query == "4. Average obesity by gender":
                # 📝 Documentation: Why include 'Both'?
                st.markdown("""
                    ### 📌 Why Include 'Both' in This Query?
                    
                    The query asks for **“Average obesity by gender”**, which implies:
                    
                    - **Male** and **Female** → direct comparisons between genders
                    - **Both** → the official **total population estimate** (population-weighted average of Male + Female)
                    
                    In public health reporting (WHO, World Bank), **'Both' is always included** because:
                    1. It represents the **true total burden** of obesity in a country or region.
                    2. It allows policymakers to understand the **overall prevalence**, not just subgroups.
                    3. Excluding 'Both' would give an incomplete picture — especially when comparing across regions or years.
                    
                    > 💡 In your data, 'Both' is nearly identical to Male and Female — this reflects global trends where male and female obesity are very similar.
                """)
                query4 = """
                    SELECT Gender, AVG(Mean_Estimate) AS Avg_Obesity
                    FROM obesity
                    WHERE Region IS NOT NULL
                    GROUP BY Gender
                    ORDER BY Avg_Obesity DESC;
                """
                df4 = run_query(query4)
                
                if not df4.empty:
                    st.table(df4)
                    
                    # Visualization: Horizontal bar chart
                    fig, ax = plt.subplots(figsize=(6, 3))
                    bars = ax.barh(df4['Gender'], df4['Avg_Obesity'], color=['steelblue', 'orange'])
                    ax.set_xlabel('Average Obesity (%)')
                    ax.set_title('Average Obesity by Gender (2012–2022)')
                    ax.grid(axis='x', alpha=0.3)
                    for bar in bars:
                        width = bar.get_width()
                        ax.text(width + 0.05, bar.get_y() + bar.get_height()/2, f'{width:.1f}%', 
                                va='center', ha='left', fontsize=9)
                    st.pyplot(fig)
                else:
                    st.write("No data found.")

            elif selected_query == "5. Country count by obesity level category and age group":
                st.subheader("Country count by obesity level category and age group")
                query5 = """
                    SELECT 
                        obesity_level,
                        age_group,
                        COUNT(DISTINCT Country) as Country_Count
                    FROM obesity
                    WHERE Region IS NOT NULL
                    GROUP BY obesity_level, age_group
                    ORDER BY age_group, obesity_level;
                """
                df5 = run_query(query5)
                
                if not df5.empty:
                    st.table(df5)
                    
                    # Visualization: Grouped bar chart
                    fig, ax = plt.subplots(figsize=(8, 4))
                    pivot = df5.pivot(index='obesity_level', columns='age_group', values='Country_Count').fillna(0)
                    pivot.plot(kind='bar', ax=ax, color=['steelblue', 'orange'])
                    ax.set_ylabel('Number of Countries')
                    ax.set_title('Country Count by Obesity Level and Age Group')
                    ax.legend(title="Age Group")
                    ax.grid(axis='y', alpha=0.3)
                    for container in ax.containers:
                        ax.bar_label(container)
                    st.pyplot(fig)
                else:
                    st.write("No data found.")

            elif selected_query == "6. Top 5 countries - least reliable & Most consistent":
                st.subheader("Top 5 Countries: Least Reliable vs Most Consistent")

                col1, col2 = st.columns(2)  # Two columns

                # ----------------------------
                # Left Column: Least Reliable (Highest CI_Width)
                # ----------------------------
                with col1:
                    st.markdown("### Least Reliable (Highest CI_Width)")
                    
                    query6a = """
                        SELECT Country, CI_Width, Mean_Estimate
                        FROM obesity
                        WHERE Year = 2022
                        AND Gender = 'Both'
                        AND age_group = 'Adult'
                        AND Region IS NOT NULL
                        ORDER BY CI_Width DESC
                        LIMIT 5;
                    """
                    df6a = run_query(query6a)
                    
                    if not df6a.empty:
                        st.table(df6a)
                        
                        # Visualization
                        fig, ax = plt.subplots(figsize=(6, 4))
                        bars = ax.barh(df6a['Country'], df6a['CI_Width'], color='steelblue')
                        ax.set_xlabel('CI Width')
                        ax.set_title('Top 5 Least Reliable Countries (2022)')
                        ax.grid(axis='x', alpha=0.3)
                        for bar in bars:
                            width = bar.get_width()
                            ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, f'{width:.2f}', 
                                    va='center', ha='left', fontsize=9)
                        st.pyplot(fig)
                    else:
                        st.write("No data found.")

                # ----------------------------
                # Right Column: Most Consistent (Smallest Average CI_Width)
                # ----------------------------
                with col2:
                    st.markdown("### Most Consistent (Smallest Average CI_Width)")
                    
                    query6b = """
                        SELECT Country, AVG(CI_Width) as Avg_CI_Width
                        FROM obesity
                        WHERE Gender = 'Both'
                        AND age_group = 'Adult'
                        AND Region IS NOT NULL
                        GROUP BY Country
                        ORDER BY Avg_CI_Width ASC
                        LIMIT 5;
                    """
                    df6b = run_query(query6b)
                    
                    if not df6b.empty:
                        st.table(df6b)
                        
                        # Visualization
                        fig, ax = plt.subplots(figsize=(6, 4))
                        bars = ax.barh(df6b['Country'], df6b['Avg_CI_Width'], color='orange')
                        ax.set_xlabel('Average CI Width')
                        ax.set_title('Top 5 Most Consistent Countries')
                        ax.grid(axis='x', alpha=0.3)
                        for bar in bars:
                            width = bar.get_width()
                            ax.text(width + 0.05, bar.get_y() + bar.get_height()/2, f'{width:.2f}', 
                                    va='center', ha='left', fontsize=9)
                        st.pyplot(fig)
                    else:
                        st.write("No data found.")

            elif selected_query == "7. Average obesity by age group":
                st.subheader("Average Obesity by Age Group")
                
                query7 = """
                    SELECT 
                        age_group,
                        AVG(Mean_Estimate) as Avg_Obesity
                    FROM obesity
                    WHERE Region IS NOT NULL
                    GROUP BY age_group
                    ORDER BY Avg_Obesity DESC;
                """
                df7 = run_query(query7)
                
                if not df7.empty:
                    st.table(df7)
                    
                    # Visualization: Horizontal bar chart
                    fig, ax = plt.subplots(figsize=(6, 3))
                    bars = ax.barh(df7['age_group'], df7['Avg_Obesity'], color=['steelblue', 'orange'])
                    ax.set_xlabel('Average Obesity (%)')
                    ax.set_title('Average Obesity by Age Group (2012–2022)')
                    ax.grid(axis='x', alpha=0.3)
                    for bar in bars:
                        width = bar.get_width()
                        ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, f'{width:.1f}%', 
                                va='center', ha='left', fontsize=9)
                    st.pyplot(fig)
                else:
                    st.write("No data found.")

            elif selected_query == "8. Top 10 Countries with consistent low obesity":
                st.subheader("Top 10 Countries with Consistent Low Obesity")
                
                query8 = """
                    SELECT 
                        Country,
                        AVG(Mean_Estimate) as Avg_Obesity,
                        AVG(CI_Width) as Avg_CI_Width
                    FROM obesity
                    WHERE Region IS NOT NULL
                    AND Gender = 'Both'
                    AND age_group = 'Adult'
                    GROUP BY Country
                    HAVING Avg_Obesity < 5.0  -- Low average
                    AND Avg_CI_Width < 1.0  -- Low variability
                    ORDER BY Avg_Obesity ASC, Avg_CI_Width ASC
                    LIMIT 10;
                """
                df8 = run_query(query8)
                
                if not df8.empty:
                    st.table(df8)
                    
                    # Visualization: Horizontal bar chart for Avg_Obesity
                    fig, ax = plt.subplots(figsize=(8, 6))
                    bars = ax.barh(df8['Country'], df8['Avg_Obesity'], color='steelblue')
                    ax.set_xlabel('Average Obesity (%)')
                    ax.set_title('Top 10 Countries with Consistent Low Obesity (Avg < 5%, CI < 1.0)')
                    ax.grid(axis='x', alpha=0.3)
                    for bar in bars:
                        width = bar.get_width()
                        ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, f'{width:.1f}%', 
                                va='center', ha='left', fontsize=9)
                    st.pyplot(fig)
                else:
                    st.write("No data found.")

            elif selected_query == "9. Countries where female obesity exceeds male by large margin (same year)":
                st.subheader("Countries where Female Obesity Exceeds Male by Large Margin")
                
                query9 = """
                    SELECT 
                        Country,
                        Year,
                        MAX(CASE WHEN Gender = 'Female' THEN Mean_Estimate END) as Female_Obesity,
                        MAX(CASE WHEN Gender = 'Male' THEN Mean_Estimate END) as Male_Obesity,
                        (MAX(CASE WHEN Gender = 'Female' THEN Mean_Estimate END) - 
                        MAX(CASE WHEN Gender = 'Male' THEN Mean_Estimate END)) as Difference
                    FROM obesity
                    WHERE Region IS NOT NULL
                    AND Gender IN ('Female', 'Male')
                    AND age_group = 'Adult'
                    GROUP BY Country, Year
                    HAVING Difference > 5.0  -- Large margin
                    ORDER BY Difference DESC
                    LIMIT 10;
                """
                df9 = run_query(query9)
                
                if not df9.empty:
                    st.table(df9)
                    
                    # Visualization: Horizontal bar chart for Difference
                    fig, ax = plt.subplots(figsize=(8, 6))
                    bars = ax.barh(df9['Country'] + ' (' + df9['Year'].astype(str) + ')', 
                                df9['Difference'], color='steelblue')
                    ax.set_xlabel('Difference (Female - Male) %')
                    ax.set_title('Top 10 Countries: Female Obesity > Male by >5%')
                    ax.grid(axis='x', alpha=0.3)
                    for bar in bars:
                        width = bar.get_width()
                        ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, f'{width:.1f}%', 
                                va='center', ha='left', fontsize=9)
                    st.pyplot(fig)
                else:
                    st.write("No data found.")

            elif selected_query == "10. Global average obesity percentage per year":
                st.subheader("Global Average Obesity Percentage per Year")
                
                query10 = """
                    SELECT 
                        Year,
                        AVG(Mean_Estimate) as Avg_Obesity
                    FROM obesity
                    WHERE Country = 'Global'
                    AND Gender = 'Both'
                    AND age_group = 'Adult'
                    GROUP BY Year
                    ORDER BY Year;
                """
                df10 = run_query(query10)
                
                if not df10.empty:
                    st.table(df10)
                    
                    # Visualization: Line chart
                    fig, ax = plt.subplots(figsize=(8, 4))
                    ax.plot(df10['Year'], df10['Avg_Obesity'], marker='o', color='steelblue')
                    ax.set_xlabel('Year')
                    ax.set_ylabel('Average Obesity (%)')
                    ax.set_title('Global Average Obesity per Year (2012–2022)')
                    ax.grid(alpha=0.3)
                    for i, row in df10.iterrows():
                        ax.text(row['Year'], row['Avg_Obesity'] + 0.1, f'{row["Avg_Obesity"]:.1f}%', 
                                ha='center', va='bottom', fontsize=9)
                    st.pyplot(fig)
                else:
                    st.write("No data found.")

        if st.session_state.category == "Malnutrition":
            if selected_query == "1. Avg. malnutrition by age group":
                st.subheader("Average Malnutrition by Age Group")
                
                malq1 = """
                    SELECT age_group, AVG(Mean_Estimate) as Avg_Malnutrition
                    FROM malnutrition
                    WHERE Region IS NOT NULL
                    GROUP BY age_group
                    ORDER BY Avg_Malnutrition DESC;
                """
                maldf1 = run_query(malq1)
                
                if not maldf1.empty:
                    st.table(maldf1)
                    
                    # Visualization: Horizontal bar chart
                    fig, ax = plt.subplots(figsize=(6, 3))
                    bars = ax.barh(maldf1['age_group'], maldf1['Avg_Malnutrition'], color=['steelblue', 'orange'])
                    ax.set_xlabel('Average Malnutrition (%)')
                    ax.set_title('Average Malnutrition by Age Group (2012–2022)')
                    ax.grid(axis='x', alpha=0.3)
                    for bar in bars:
                        width = bar.get_width()
                        ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, f'{width:.1f}%', 
                                va='center', ha='left', fontsize=9)
                    st.pyplot(fig)
                else:
                    st.write("No data found.")
            
            elif selected_query == "2. Top 5 countries with highest malnutrition (mean_estimate)":
                st.subheader("Top 5 Countries with Highest Malnutrition (2022)")
                
                query2 = """
                    SELECT Country, Mean_Estimate
                    FROM malnutrition
                    WHERE Year = 2022
                      AND Gender = 'Both'
                      AND age_group = 'Adult'
                      AND Region IS NOT NULL
                    ORDER BY Mean_Estimate DESC
                    LIMIT 5;
                """
                df2 = run_query(query2)
                
                if not df2.empty:
                    st.table(df2)
                    
                    # Visualization: Horizontal bar chart
                    fig, ax = plt.subplots(figsize=(8, 4))
                    bars = ax.barh(df2['Country'], df2['Mean_Estimate'], color='steelblue')
                    ax.set_xlabel('Malnutrition (%)')
                    ax.set_title('Top 5 Countries with Highest Malnutrition (2022)')
                    ax.grid(axis='x', alpha=0.3)
                    for bar in bars:
                        width = bar.get_width()
                        ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, f'{width:.1f}%', 
                                va='center', ha='left', fontsize=9)
                    st.pyplot(fig)
                else:
                    st.write("No data found.")            
            
            elif selected_query == "3. Malnutrition trend in African region over the years":
                st.subheader("Malnutrition Trend in African Region over the Years")
                
                query3 = """
                    SELECT 
                        Year,
                        AVG(Mean_Estimate) as Avg_Malnutrition
                    FROM malnutrition
                    WHERE Region = 'Africa'
                      AND Gender = 'Both'
                      AND age_group = 'Adult'
                    GROUP BY Year
                    ORDER BY Year;
                """
                df3 = run_query(query3)
                
                if not df3.empty:
                    st.table(df3)
                    
                    # Visualization: Line chart
                    fig, ax = plt.subplots(figsize=(8, 4))
                    ax.plot(df3['Year'], df3['Avg_Malnutrition'], marker='o', color='steelblue')
                    ax.set_xlabel('Year')
                    ax.set_ylabel('Average Malnutrition (%)')
                    ax.set_title('Malnutrition Trend in Africa (2012–2022)')
                    ax.grid(alpha=0.3)
                    for i, row in df3.iterrows():
                        ax.text(row['Year'], row['Avg_Malnutrition'] + 0.1, f"{row['Avg_Malnutrition']:.1f}%", 
                                ha='center', va='bottom', fontsize=8)
                    st.pyplot(fig)
                else:
                    st.write("No data found for Africa.")
            
            elif selected_query == "4. Gender-based average malnutrition":
                st.subheader("Gender-Based Average Malnutrition")
                
                query4 = """
                    SELECT 
                        Gender,
                        AVG(Mean_Estimate) as Avg_Malnutrition
                    FROM malnutrition
                    WHERE Region IS NOT NULL
                    GROUP BY Gender
                    ORDER BY Avg_Malnutrition DESC;
                """
                df4 = run_query(query4)
                
                if not df4.empty:
                    st.table(df4)
                    
                    # Visualization: Horizontal bar chart
                    fig, ax = plt.subplots(figsize=(6, 3))
                    bars = ax.barh(df4['Gender'], df4['Avg_Malnutrition'], color=['steelblue', 'orange'])
                    ax.set_xlabel('Average Malnutrition (%)')
                    ax.set_title('Average Malnutrition by Gender (2012–2022)')
                    ax.grid(axis='x', alpha=0.3)
                    for bar in bars:
                        width = bar.get_width()
                        ax.text(width + 0.05, bar.get_y() + bar.get_height()/2, f'{width:.1f}%', 
                                va='center', ha='left', fontsize=9)
                    st.pyplot(fig)
                else:
                    st.write("No data found.")
            
            elif selected_query == "5. Malnutrition level-wise (average CI_Width by age group)":
                st.subheader("Average CI Width by Malnutrition Level and Age Group")
                
                query5 = """
                    SELECT 
                        malnutrition_level,
                        age_group,
                        AVG(CI_Width) as Avg_CI_Width
                    FROM malnutrition
                    WHERE Region IS NOT NULL
                    GROUP BY malnutrition_level, age_group
                    ORDER BY age_group, malnutrition_level;
                """
                df5 = run_query(query5)
                
                if not df5.empty:
                    st.table(df5)
                    
                    # Visualization: Grouped bar chart
                    fig, ax = plt.subplots(figsize=(8, 4))
                    pivot = df5.pivot(index='malnutrition_level', columns='age_group', values='Avg_CI_Width').fillna(0)
                    pivot.plot(kind='bar', ax=ax, color=['steelblue', 'orange'])
                    ax.set_ylabel('Average CI Width')
                    ax.set_title('Average CI Width by Malnutrition Level and Age Group')
                    ax.legend(title="Age Group")
                    ax.grid(axis='y', alpha=0.3)
                    for container in ax.containers:
                        ax.bar_label(container)
                    st.pyplot(fig)
                else:
                    st.write("No data found.")            
            
            elif selected_query == "6. Yearly malnutrition change in specific countries (India, Nigeria, Brazil)":
                st.subheader("Yearly Malnutrition Change in India, Nigeria, and Brazil")
                
                query6 = """
                    SELECT 
                        Country,
                        Year,
                        Mean_Estimate as Malnutrition
                    FROM malnutrition
                    WHERE Country IN ('India', 'Nigeria', 'Brazil')
                      AND Gender = 'Both'
                      AND age_group = 'Adult'
                    ORDER BY Country, Year;
                """
                df6 = run_query(query6)
                
                if not df6.empty:
                    
                    
                    # Visualization: Line chart for each country
                    fig, ax = plt.subplots(figsize=(8, 4))
                    for country in ['India', 'Nigeria', 'Brazil']:
                        subset = df6[df6['Country'] == country]
                        ax.plot(subset['Year'], subset['Malnutrition'], marker='o', label=country)
                    ax.set_xlabel('Year')
                    ax.set_ylabel('Malnutrition (%)')
                    ax.set_title('Yearly Malnutrition Change in India, Nigeria, Brazil (2012–2022)')
                    ax.legend()
                    ax.grid(alpha=0.3)
                    st.pyplot(fig)
                    st.table(df6)
                else:
                    st.write("No data found for these countries.")            
            
            elif selected_query == "7. Regions with lowest malnutrition averages":
                st.subheader("Regions with Lowest Malnutrition Averages")
                
                query7 = """
                    SELECT 
                        Region,
                        AVG(Mean_Estimate) as Avg_Malnutrition
                    FROM malnutrition
                    WHERE Region IS NOT NULL
                      AND Gender = 'Both'
                      AND age_group = 'Adult'
                    GROUP BY Region
                    ORDER BY Avg_Malnutrition ASC
                    LIMIT 5;
                """
                df7 = run_query(query7)
                
                if not df7.empty:
                    st.table(df7)
                    
                    # Visualization: Horizontal bar chart
                    fig, ax = plt.subplots(figsize=(8, 4))
                    bars = ax.barh(df7['Region'], df7['Avg_Malnutrition'], color='steelblue')
                    ax.set_xlabel('Average Malnutrition (%)')
                    ax.set_title('Top 5 Regions with Lowest Malnutrition (2012–2022)')
                    ax.grid(axis='x', alpha=0.3)
                    for bar in bars:
                        width = bar.get_width()
                        ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, f'{width:.1f}%', 
                                va='center', ha='left', fontsize=9)
                    st.pyplot(fig)
                else:
                    st.write("No data found.")            
            
            elif selected_query == "8. Countries with increasing malnutrition":
                st.subheader("Countries with Increasing Malnutrition")
                
                query8 = """
                    SELECT 
                        Country,
                        MIN(Year) as First_Year,
                        MAX(Year) as Last_Year,
                        MIN(Mean_Estimate) as Min_Malnutrition,
                        MAX(Mean_Estimate) as Max_Malnutrition,
                        (MAX(Mean_Estimate) - MIN(Mean_Estimate)) as Increase
                    FROM malnutrition
                    WHERE Region IS NOT NULL
                      AND Gender = 'Both'
                      AND age_group = 'Adult'
                    GROUP BY Country
                    HAVING Increase > 0  -- Increasing trend
                    ORDER BY Increase DESC
                    LIMIT 10;
                """
                df8 = run_query(query8)
                
                if not df8.empty:
                    st.table(df8)
                    
                    # Visualization: Horizontal bar chart for Increase
                    fig, ax = plt.subplots(figsize=(8, 6))
                    bars = ax.barh(df8['Country'], df8['Increase'], color='steelblue')
                    ax.set_xlabel('Increase in Malnutrition (%)')
                    ax.set_title('Top 10 Countries with Increasing Malnutrition (2012–2022)')
                    ax.grid(axis='x', alpha=0.3)
                    for bar in bars:
                        width = bar.get_width()
                        ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, f'{width:.1f}%', 
                                va='center', ha='left', fontsize=9)
                    st.pyplot(fig)
                else:
                    st.write("No data found.")            

            elif selected_query == "9. Min/Max malnutrition levels year-wise comparison":
                st.subheader("Min/Max Malnutrition Levels Year-Wise")
                
                query9 = """
                    SELECT 
                        Year,
                        MIN(Mean_Estimate) as Min_Malnutrition,
                        MAX(Mean_Estimate) as Max_Malnutrition
                    FROM malnutrition
                    WHERE Region IS NOT NULL
                      AND Gender = 'Both'
                      AND age_group = 'Adult'
                    GROUP BY Year
                    ORDER BY Year;
                """
                df9 = run_query(query9)
                
                if not df9.empty:
                    st.table(df9)
                    
                    # Visualization: Line chart for Min and Max
                    fig, ax = plt.subplots(figsize=(8, 4))
                    ax.plot(df9['Year'], df9['Min_Malnutrition'], marker='o', color='steelblue', label='Min')
                    ax.plot(df9['Year'], df9['Max_Malnutrition'], marker='o', color='orange', label='Max')
                    ax.set_xlabel('Year')
                    ax.set_ylabel('Malnutrition (%)')
                    ax.set_title('Min/Max Malnutrition Levels by Year (2012–2022)')
                    ax.legend()
                    ax.grid(alpha=0.3)
                    st.pyplot(fig)
                else:
                    st.write("No data found.")
            
            elif selected_query == "10. High CI_Width flags for monitoring (CI_width > 5)":
                st.subheader("Countries with High CI_Width (CI_Width > 5)")
                
                query10 = """
                    SELECT 
                        Country,
                        MAX(Year) as Year,
                        AVG(Mean_Estimate) as Malnutrition,
                        MAX(CI_Width) as CI_Width
                    FROM malnutrition
                    WHERE Region IS NOT NULL
                    AND Gender = 'Both'
                    AND age_group = 'Adult'
                    AND CI_Width > 5.0
                    GROUP BY Country
                    ORDER BY CI_Width DESC
                    LIMIT 10;
                """
                df10 = run_query(query10)
                
                if not df10.empty:
                    st.table(df10)
                    
                    # Visualization: Horizontal bar chart for CI_Width
                    fig, ax = plt.subplots(figsize=(8, 6))
                    bars = ax.barh(df10['Country'] + ' (' + df10['Year'].astype(str) + ')', 
                                   df10['CI_Width'], color='steelblue')
                    ax.set_xlabel('CI Width')
                    ax.set_title('Top 10 Countries with High CI_Width (CI > 5.0)')
                    ax.grid(axis='x', alpha=0.3)
                    for bar in bars:
                        width = bar.get_width()
                        ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, f'{width:.2f}', 
                                va='center', ha='left', fontsize=9)
                    st.pyplot(fig)
                else:
                    st.write("No data found.")


            else:
                st.write("Please select a query to run.")

        if st.session_state.category == "Combined":
            
            if selected_query == "1. Obesity vs malnutrition comparison by country (any 5 countries)":

                st.subheader("Obesity vs Malnutrition Comparison by Country")
                
                query1 = """
                    SELECT 
                        o.Country,
                        o.Mean_Estimate as Obesity,
                        m.Mean_Estimate as Malnutrition
                    FROM obesity o
                    JOIN malnutrition m 
                      ON o.Country = m.Country 
                     AND o.Year = m.Year 
                     AND o.Gender = m.Gender 
                     AND o.age_group = m.age_group
                    WHERE o.Year = 2022
                      AND o.Gender = 'Both'
                      AND o.age_group = 'Adult'
                      AND o.Country IN ('India', 'Nigeria', 'Brazil', 'USA', 'China')
                    ORDER BY o.Country;
                """
                df1 = run_query(query1)
                
                if not df1.empty:
                    st.table(df1)
                    
                    # Visualization: Grouped bar chart
                    fig, ax = plt.subplots(figsize=(8, 4))
                    x = range(len(df1['Country']))
                    width = 0.35
                    
                    bars1 = ax.bar(x, df1['Obesity'], width, label='Obesity', color='steelblue')
                    bars2 = ax.bar([i + width for i in x], df1['Malnutrition'], width, label='Malnutrition', color='orange')
                    
                    ax.set_xlabel('Country')
                    ax.set_ylabel('Percentage (%)')
                    ax.set_title('Obesity vs Malnutrition in 2022 (Adult, Both)')
                    ax.set_xticks([i + width / 2 for i in x])
                    ax.set_xticklabels(df1['Country'])
                    ax.legend()
                    ax.grid(axis='y', alpha=0.3)
                    
                    # Add value labels
                    for bar in bars1:
                        height = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.1, f'{height:.1f}%', 
                                ha='center', va='bottom', fontsize=8)
                    for bar in bars2:
                        height = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.1, f'{height:.1f}%', 
                                ha='center', va='bottom', fontsize=8)
                    
                    st.pyplot(fig)
                else:
                    st.write("No data found for these countries.")

            elif selected_query == "2. Gender-based disparity in both obesity and malnutrition":
                st.subheader("Gender-Based Disparity in Obesity and Malnutrition")
                
                query2 = """
                    SELECT 
                        o.Gender,
                        AVG(o.Mean_Estimate) as Avg_Obesity,
                        AVG(m.Mean_Estimate) as Avg_Malnutrition
                    FROM obesity o
                    JOIN malnutrition m 
                      ON o.Country = m.Country 
                     AND o.Year = m.Year 
                     AND o.Gender = m.Gender 
                     AND o.age_group = m.age_group
                    WHERE o.Year = 2022
                      AND o.Gender IN ('Male', 'Female')
                      AND o.age_group = 'Adult'
                      AND o.Region IS NOT NULL  -- ✅ Safety: Only real countries
                      AND m.Region IS NOT NULL  -- ✅ Safety: Only real countries
                    GROUP BY o.Gender
                    ORDER BY o.Gender;
                """
                df2 = run_query(query2)
                
                if not df2.empty:
                    st.table(df2)
                    
                    # Visualization: Grouped bar chart
                    fig, ax = plt.subplots(figsize=(8, 4))
                    x = range(len(df2['Gender']))
                    width = 0.35
                    
                    bars1 = ax.bar(x, df2['Avg_Obesity'], width, label='Obesity', color='steelblue')
                    bars2 = ax.bar([i + width for i in x], df2['Avg_Malnutrition'], width, label='Malnutrition', color='orange')
                    
                    ax.set_xlabel('Gender')
                    ax.set_ylabel('Percentage (%)')
                    ax.set_title('Gender-Based Disparity in Obesity and Malnutrition (2022)')
                    ax.set_xticks([i + width / 2 for i in x])
                    ax.set_xticklabels(df2['Gender'])
                    ax.legend()
                    ax.grid(axis='y', alpha=0.3)
                    
                    # Add value labels
                    for bar in bars1:
                        height = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.1, f'{height:.1f}%', 
                                ha='center', va='bottom', fontsize=8)
                    for bar in bars2:
                        height = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.1, f'{height:.1f}%', 
                                ha='center', va='bottom', fontsize=8)
                    
                    st.pyplot(fig)
                else:
                    st.write("No data found.")

            elif selected_query == "3. Region-wise avg estimates side-by-side (Africa and America)":
                st.subheader("Region-wise Average Estimates: Africa vs Americas")
                
                query3 = """
                    SELECT 
                        'Africa' as Region,
                        AVG(o.Mean_Estimate) as Avg_Obesity,
                        AVG(m.Mean_Estimate) as Avg_Malnutrition
                    FROM obesity o
                    JOIN malnutrition m 
                      ON o.Country = m.Country 
                     AND o.Year = m.Year 
                     AND o.Gender = m.Gender 
                     AND o.age_group = m.age_group
                    WHERE o.Region = 'Africa'
                      AND o.Gender = 'Both'
                      AND o.age_group = 'Adult'
                      AND o.Region IS NOT NULL
                      AND m.Region IS NOT NULL
                    
                    UNION ALL
                    
                    SELECT 
                        'Americas' as Region,
                        AVG(o.Mean_Estimate) as Avg_Obesity,
                        AVG(m.Mean_Estimate) as Avg_Malnutrition
                    FROM obesity o
                    JOIN malnutrition m 
                      ON o.Country = m.Country 
                     AND o.Year = m.Year 
                     AND o.Gender = m.Gender 
                     AND o.age_group = m.age_group
                    WHERE o.Region = 'Americas'
                      AND o.Gender = 'Both'
                      AND o.age_group = 'Adult'
                      AND o.Region IS NOT NULL
                      AND m.Region IS NOT NULL;
                """
                df3 = run_query(query3)
                
                if not df3.empty:
                    st.table(df3)
                    
                    # Visualization: Grouped bar chart
                    fig, ax = plt.subplots(figsize=(8, 4))
                    x = range(len(df3['Region']))
                    width = 0.35
                    
                    bars1 = ax.bar(x, df3['Avg_Obesity'], width, label='Obesity', color='steelblue')
                    bars2 = ax.bar([i + width for i in x], df3['Avg_Malnutrition'], width, label='Malnutrition', color='orange')
                    
                    ax.set_xlabel('Region')
                    ax.set_ylabel('Percentage (%)')
                    ax.set_title('Average Obesity and Malnutrition: Africa vs Americas (2012–2022)')
                    ax.set_xticks([i + width / 2 for i in x])
                    ax.set_xticklabels(df3['Region'])
                    ax.legend()
                    ax.grid(axis='y', alpha=0.3)
                    
                    # Add value labels
                    for bar in bars1:
                        height = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.1, f'{height:.1f}%', 
                                ha='center', va='bottom', fontsize=8)
                    for bar in bars2:
                        height = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.1, f'{height:.1f}%', 
                                ha='center', va='bottom', fontsize=8)
                    
                    st.pyplot(fig)
                else:
                    st.write("No data found for these regions.")

            elif selected_query == "4. Countries with obesity up & malnutrition down":
                st.subheader("Countries with Increasing Obesity and Decreasing Malnutrition")
                
                query4 = """
                    SELECT 
                        o.Country,
                        AVG(o.Mean_Estimate) as Avg_Obesity,
                        AVG(m.Mean_Estimate) as Avg_Malnutrition
                    FROM obesity o
                    JOIN malnutrition m 
                      ON o.Country = m.Country 
                     AND o.Year = m.Year 
                     AND o.Gender = m.Gender 
                     AND o.age_group = m.age_group
                    WHERE o.Gender = 'Both'
                      AND o.age_group = 'Adult'
                      AND o.Region IS NOT NULL
                      AND m.Region IS NOT NULL
                    GROUP BY o.Country
                    HAVING AVG(o.Mean_Estimate) > 15.0  -- High obesity
                       AND AVG(m.Mean_Estimate) < 10.0  -- Low malnutrition
                    ORDER BY Avg_Obesity DESC, Avg_Malnutrition ASC
                    LIMIT 10;
                """
                df4 = run_query(query4)
                
                if not df4.empty:
                    st.table(df4)
                    
                    # Visualization: Scatter plot
                    fig, ax = plt.subplots(figsize=(8, 6))
                    scatter = ax.scatter(df4['Avg_Obesity'], df4['Avg_Malnutrition'], 
                                         c=df4['Avg_Obesity'] - df4['Avg_Malnutrition'], 
                                         cmap='viridis', s=100, edgecolor='k')
                    ax.set_xlabel('Average Obesity (%)')
                    ax.set_ylabel('Average Malnutrition (%)')
                    ax.set_title('Countries with High Obesity & Low Malnutrition (2012–2022)')
                    ax.grid(alpha=0.3)
                    
                    # Add country labels
                    for i, row in df4.iterrows():
                        ax.text(row['Avg_Obesity'], row['Avg_Malnutrition'], row['Country'], 
                                ha='center', va='bottom', fontsize=8)
                    
                    # Colorbar
                    plt.colorbar(scatter, ax=ax, label='Obesity - Malnutrition')
                    st.pyplot(fig)
                else:
                    st.write("No data found.")

            elif selected_query == "5. Age-wise trend analysis":
                st.subheader("Age-Wise Trend Analysis: Obesity vs Malnutrition (2012–2022)")
                
                query5 = """
                    SELECT 
                        o.Year,
                        o.age_group,
                        AVG(o.Mean_Estimate) as Avg_Obesity,
                        AVG(m.Mean_Estimate) as Avg_Malnutrition
                    FROM obesity o
                    JOIN malnutrition m 
                      ON o.Country = m.Country 
                     AND o.Year = m.Year 
                     AND o.Gender = m.Gender 
                     AND o.age_group = m.age_group
                    WHERE o.Gender = 'Both'
                      AND o.age_group IN ('Adult', 'Child/Adolescent')
                      AND o.Region IS NOT NULL
                      AND m.Region IS NOT NULL
                    GROUP BY o.Year, o.age_group
                    ORDER BY o.Year, o.age_group;
                """
                df5 = run_query(query5)
                
                if not df5.empty:
                    
                    # Visualization: Two line charts (one per age group)
                    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
                    
                    # Adult
                    adult_data = df5[df5['age_group'] == 'Adult']
                    ax1.plot(adult_data['Year'], adult_data['Avg_Obesity'], marker='o', color='steelblue', label='Obesity')
                    ax1.plot(adult_data['Year'], adult_data['Avg_Malnutrition'], marker='o', color='orange', label='Malnutrition')
                    ax1.set_title('Adults: Obesity vs Malnutrition (2012–2022)')
                    ax1.set_ylabel('Percentage (%)')
                    ax1.legend()
                    ax1.grid(alpha=0.3)
                    for i, row in adult_data.iterrows():
                        ax1.text(row['Year'], row['Avg_Obesity'] + 0.1, f"{row['Avg_Obesity']:.1f}%", 
                                ha='center', va='bottom', fontsize=8)
                        ax1.text(row['Year'], row['Avg_Malnutrition'] + 0.1, f"{row['Avg_Malnutrition']:.1f}%", 
                                ha='center', va='bottom', fontsize=8)
                    
                    # Child/Adolescent
                    child_data = df5[df5['age_group'] == 'Child/Adolescent']
                    ax2.plot(child_data['Year'], child_data['Avg_Obesity'], marker='o', color='steelblue', label='Obesity')
                    ax2.plot(child_data['Year'], child_data['Avg_Malnutrition'], marker='o', color='orange', label='Malnutrition')
                    ax2.set_title('Children: Obesity vs Malnutrition (2012–2022)')
                    ax2.set_xlabel('Year')
                    ax2.set_ylabel('Percentage (%)')
                    ax2.legend()
                    ax2.grid(alpha=0.3)
                    for i, row in child_data.iterrows():
                        ax2.text(row['Year'], row['Avg_Obesity'] + 0.1, f"{row['Avg_Obesity']:.1f}%", 
                                ha='center', va='bottom', fontsize=8)
                        ax2.text(row['Year'], row['Avg_Malnutrition'] + 0.1, f"{row['Avg_Malnutrition']:.1f}%", 
                                ha='center', va='bottom', fontsize=8)
                    
                    st.pyplot(fig)
                    st.table(df5)
                else:
                    st.write("No data found.")






