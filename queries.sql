-- obesity queries 
-- 1. Top 5 regions with the highest average obesity levels in the most recent year(2022)
SELECT Region, AVG(Mean_Estimate) AS Avg_Obesity
FROM obesity
WHERE Year = 2022 AND Region IS NOT NULL
GROUP BY Region
ORDER BY Avg_Obesity DESC
LIMIT 5;
-- 2. Top 5 countries with highest obesity estimates
SELECT Country, Mean_Estimate
FROM obesity
WHERE Year = 2022 AND Gender = 'Both' AND age_group = 'Adult' AND Region IS NOT NULL
ORDER BY Mean_Estimate DESC
LIMIT 5;
-- 3. Obesity trend in India over the years(Mean_estimate)
SELECT Year, Mean_Estimate
FROM obesity
WHERE Country = 'India' AND Gender = 'Both' AND age_group = 'Adult'
ORDER BY Year; 
-- 4. Average obesity by gender
SELECT Gender, AVG(Mean_Estimate) AS Avg_Obesity
FROM obesity
WHERE Region IS NOT NULL
GROUP BY Gender
ORDER BY Avg_Obesity DESC;
-- 5. Country count by obesity level category and age group
SELECT obesity_level, age_group, COUNT(DISTINCT Country) as Country_Count
FROM obesity
WHERE Region IS NOT NULL
GROUP BY obesity_level, age_group
ORDER BY age_group, obesity_level;
-- 6. Top 5 countries least reliable countries(with highest CI_Width) and Top 5 most consistent countries (smallest average CI_Width)
SELECT Country, CI_Width, Mean_Estimate
FROM obesity
WHERE Year = 2022 AND Gender = 'Both' AND age_group = 'Adult' AND Region IS NOT NULL
ORDER BY CI_Width DESC
LIMIT 5;
                        
SELECT Country, AVG(CI_Width) as Avg_CI_Width
FROM obesity
WHERE Gender = 'Both' AND age_group = 'Adult'AND Region IS NOT NULL
GROUP BY Country
ORDER BY Avg_CI_Width ASC
LIMIT 5;
-- 7. Average obesity by age group
SELECT age_group, AVG(Mean_Estimate) as Avg_Obesity
FROM obesity
WHERE Region IS NOT NULL
GROUP BY age_group
ORDER BY Avg_Obesity DESC;
-- 8. Top 10 Countries with consistent low obesity (low average + low CI)over the years
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
-- 9. Countries where female obesity exceeds male by large margin (same       year)
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
-- 10. Global average obesity percentage per year
SELECT 
                        Year,
                        AVG(Mean_Estimate) as Avg_Obesity
                    FROM obesity
                    WHERE Country = 'Global'
                    AND Gender = 'Both'
                    AND age_group = 'Adult'
                    GROUP BY Year
                    ORDER BY Year;

----------------------------------------------------------------
-- malnutrition queries
-- 1. average malnutrition by age group
SELECT age_group, AVG(Mean_Estimate) as Avg_Malnutrition
FROM malnutrition
WHERE Region IS NOT NULL
GROUP BY age_group
ORDER BY Avg_Malnutrition DESC;

-- 2. Top 5 countries with highest malnutrition (mean_estimate)
SELECT Country, Mean_Estimate
FROM malnutrition
WHERE Year = 2022
AND Gender = 'Both'
AND age_group = 'Adult'
AND Region IS NOT NULL
ORDER BY Mean_Estimate DESC
LIMIT 5;
				
-- 3. Malnutrition trend in African region over the years
SELECT Year, AVG(Mean_Estimate) as Avg_Malnutrition
FROM malnutrition
WHERE Region = 'Africa'
AND Gender = 'Both'
AND age_group = 'Adult' 
GROUP BY Year
ORDER BY Year;

-- 4. Gender-based average malnutrition
SELECT Gender, AVG(Mean_Estimate) as Avg_Malnutrition
FROM malnutrition
WHERE Region IS NOT NULL
GROUP BY Gender
ORDER BY Avg_Malnutrition DESC;

-- 5. Malnutrition level-wise (average CI_Width by age group)
SELECT malnutrition_level, age_group, AVG(CI_Width) as Avg_CI_Width
FROM malnutrition
WHERE Region IS NOT NULL
GROUP BY malnutrition_level, age_group
ORDER BY age_group, malnutrition_level;
-- 6. Yearly malnutrition change in specific countries(India, Nigeria, Brazil)
SELECT Country, Year, Mean_Estimate as Malnutrition
FROM malnutrition
WHERE Country IN ('India', 'Nigeria', 'Brazil') AND Gender = 'Both' AND age_group = 'Adult'
ORDER BY Country, Year;

-- 7. Regions with lowest malnutrition averages
SELECT Region, AVG(Mean_Estimate) as Avg_Malnutrition
FROM malnutrition
WHERE Region IS NOT NULL AND Gender = 'Both' AND age_group = 'Adult'
GROUP BY Region
ORDER BY Avg_Malnutrition ASC
LIMIT 5;

-- 8. Countries with increasing malnutrition (💡 Hint: Use MIN() and MAX()   on Mean_Estimate per country to compare early vs. recent malnutrition levels, and filter where the difference is positive using HAVING.)
SELECT Country, 
	MIN(Year) as First_Year, MAX(Year) as Last_Year, 
    MIN(Mean_Estimate) as Min_Malnutrition,
	MAX(Mean_Estimate) as Max_Malnutrition,
	(MAX(Mean_Estimate) - MIN(Mean_Estimate)) as Increase
FROM malnutrition
WHERE Region IS NOT NULL AND Gender = 'Both' AND age_group = 'Adult'
GROUP BY Country
HAVING Increase > 0  -- Increasing trend
ORDER BY Increase DESC
LIMIT 10;

-- 9.   Min/Max malnutrition levels year-wise comparison
SELECT Year, MIN(Mean_Estimate) as Min_Malnutrition, MAX(Mean_Estimate) as Max_Malnutrition
FROM malnutrition
WHERE Region IS NOT NULL AND Gender = 'Both' AND age_group = 'Adult'
GROUP BY Year
ORDER BY Year;

-- 10.  High CI_Width flags for monitoring(CI_width > 5)
SELECT Country, Year, Mean_Estimate as Malnutrition, CI_Width 
FROM malnutrition
WHERE Region IS NOT NULL AND Gender = 'Both' AND age_group = 'Adult' AND CI_Width > 5.0
ORDER BY CI_Width DESC
LIMIT 10;

-- -- -- -- -- -- -- --
-- Combined obesity and malnutrition queries
-- 1. Obesity vs malnutrition comparison by country (any 5 countries)

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

-- 2. Gender-based disparity in both obesity and malnutrition
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

-- 3. Region-wise avg estimates side-by-side (Africa and America)

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

-- 4. Countries with obesity up & malnutrition down
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

-- 5. Age-wise trend analysis
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