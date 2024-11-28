# Project Plan

## Title
The Impact of Hurricanes on U.S. Housing Markets

## Main Question
How do hurricanes impact housing market dynamics in affected U.S. cities, particularly regarding median sale prices and housing inventory?

## Description
This project analyzes the relationship between hurricane landfalls and housing market changes in U.S. cities. By merging detailed data on hurricanes with housing market metrics, the aim is to identify trends and assess how natural disasters influence real estate. The project involves building an automated ETL pipeline, conducting data analysis, and producing visualizations to support conclusions.

## Data Sources

### Datasource #1: U.S. Hurricanes and Landfalls 1851-2023
- **Metadata URL**: [Kaggle - U.S. Hurricanes Dataset](https://www.kaggle.com/datasets/sandraroko/u-s-hurricanes-and-landfalls-1851-2023)
- **Data Type**: CSV
- **License**: CC0: Public Domain
- **Description**: This dataset provides records of hurricanes, including names, dates, locations, and intensities. It enables the identification of hurricanes affecting specific regions and their characteristics.

### Datasource #2: U.S. Cities Housing Market Data
- **Metadata URL**: [Kaggle - U.S. Housing Market Data](https://www.kaggle.com/datasets/vincentvaseghi/us-cities-housing-market-data)
- **Data Type**: CSV
- **License**: CC0: Public Domain
- **Description**: This dataset offers monthly statistics for housing markets, such as median sale prices, housing inventory, and days on the market. It helps evaluate changes in the housing market pre- and post-hurricane events.

## Work Packages

1. **Data Collection and Understanding**  
   Gather and validate datasets for quality and relevance to the research question.

2. **ETL Pipeline Development**  
   Develop an automated ETL pipeline to extract, clean, and store the data. Address missing values, normalize formats, and filter unnecessary columns.

3. **Data Merging and Transformation**  
   Merge datasets based on location and time, ensuring consistency and quality. Handle multi-value fields (e.g., "State Affected") by creating multiple rows or using other strategies.

4. **Exploratory Data Analysis (EDA)**  
   Analyze trends and patterns in the data to understand hurricane impacts. Visualize key metrics like sale price changes and inventory levels.

5. **Final Analysis and Visualization**  
   Conduct deeper statistical analysis and create visualizations that communicate findings effectively.

6. **Report Writing**  
   Document the entire process and findings in a detailed report. Reflect on limitations and suggest further research directions.
  



