import json
import pandas as pd
import matplotlib.pyplot as plt

# Load data from JSON file
with open('examples/zinc/data/database.json') as f:
    data = json.load(f)

print(f"Data type: {type(data)}")
print(f"First few items: {data[:5]}")

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Extract zinc values and food groups
zinc_values = []
food_groups = []
for item in data:
    food_groups.append(item['group'])
    for nutrient in item['nutrients']:
        if nutrient['description'] == 'Zinc, Zn':
            zinc_values.append(nutrient['value'])
            break
    else:
        zinc_values.append(None)

# Create a new DataFrame with zinc values and food groups
df_zinc = pd.DataFrame({
    'Food Group': food_groups,
    'Zinc Value': zinc_values
})

print(f"Zinc Data Shape:\n{df_zinc.shape}")
print(f"Zinc Column Names:\n{df_zinc.columns.tolist()}")
print(f"Zinc Data Types:\n{df_zinc.dtypes}")
print(f"First few rows of Zinc Data:\n{df_zinc.head()}")

# Calculate median zinc value by food group
zinc_median = df_zinc.groupby('Food Group')['Zinc Value'].median()
print(f"Median Zinc Value by Food Group:\n{zinc_median}")

# Create a new DataFrame with median zinc values
zinc_median_df = zinc_median.to_frame('Median Zinc Value').reset_index()
print(f"Median Zinc Value DataFrame Shape:\n{zinc_median_df.shape}")
print(f"Median Zinc Value DataFrame Column Names:\n{zinc_median_df.columns.tolist()}")
print(f"Median Zinc Value DataFrame Types:\n{zinc_median_df.dtypes}")
print(f"First few rows of Median Zinc Value DataFrame:\n{zinc_median_df.head()}")

# Plot median zinc values by food group
plt.figure(figsize=(10,6))
plt.bar(zinc_median_df['Food Group'], zinc_median_df['Median Zinc Value'])
plt.xlabel('Food Group')
plt.ylabel('Median Zinc Value')
plt.title('Median Zinc Value by Food Group')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# Plot median zinc values by food group in descending order
zinc_median_df_copy = zinc_median_df.copy()
zinc_median_df_copy = zinc_median_df_copy.sort_values(by='Median Zinc Value', ascending=False)
plt.figure(figsize=(10,6))
plt.bar(zinc_median_df_copy['Food Group'], zinc_median_df_copy['Median Zinc Value'])
plt.xlabel('Food Group')
plt.ylabel('Median Zinc Value')
plt.title('Median Zinc Value by Food Group (Descending Order)')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# Plot top 10 median zinc values by food group in descending order
top_10 = zinc_median_df_copy.head(10)
plt.figure(figsize=(10,6))
plt.bar(top_10['Food Group'], top_10['Median Zinc Value'])
plt.xlabel('Food Group')
plt.ylabel('Median Zinc Value')
plt.title('Top 10 Median Zinc Value by Food Group (Descending Order)')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# Calculate mean zinc value by food group
zinc_mean = df_zinc.groupby('Food Group')['Zinc Value'].mean()
print(f"Mean Zinc Value by Food Group:\n{zinc_mean}")

# Create a new DataFrame with mean zinc values
zinc_mean_df = zinc_mean.to_frame('Mean Zinc Value').reset_index()
print(f"Mean Zinc Value DataFrame Shape:\n{zinc_mean_df.shape}")
print(f"Mean Zinc Value DataFrame Column Names:\n{zinc_mean_df.columns.tolist()}")
print(f"Mean Zinc Value DataFrame Types:\n{zinc_mean_df.dtypes}")
print(f"First few rows of Mean Zinc Value DataFrame:\n{zinc_mean_df.head()}")

# Plot mean zinc values by food group in descending order
zinc_mean_df_copy = zinc_mean_df.copy()
zinc_mean_df_copy = zinc_mean_df_copy.sort_values(by='Mean Zinc Value', ascending=False)
plt.figure(figsize=(10,6))
plt.bar(zinc_mean_df_copy['Food Group'], zinc_mean_df_copy['Mean Zinc Value'])
plt.xlabel('Food Group')
plt.ylabel('Mean Zinc Value')
plt.title('Mean Zinc Value by Food Group (Descending Order)')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# Calculate standard deviation of zinc values by food group
zinc_std = df_zinc.groupby('Food Group')['Zinc Value'].std()
print(f"Standard Deviation of Zinc Values by Food Group:\n{zinc_std}")

# Create a new DataFrame with standard deviations
zinc_std_df = zinc_std.to_frame('Standard Deviation of Zinc Values').reset_index()
print(f"Standard Deviation of Zinc Values DataFrame Shape:\n{zinc_std_df.shape}")
print(f"Standard Deviation of Zinc Values DataFrame Column Names:\n{zinc_std_df.columns.tolist()}")
print(f"Standard Deviation of Zinc Values DataFrame Types:\n{zinc_std_df.dtypes}")
print(f"First few rows of Standard Deviation of Zinc Values DataFrame:\n{zinc_std_df.head()}")

# Plot standard deviations of zinc values by food group in descending order
zinc_std_df_copy = zinc_std_df.copy()
zinc_std_df_copy = zinc_std_df_copy.sort_values(by='Standard Deviation of Zinc Values', ascending=False)
plt.figure(figsize=(10,6))
plt.bar(zinc_std_df_copy['Food Group'], zinc_std_df_copy['Standard Deviation of Zinc Values'])
plt.xlabel('Food Group')
plt.ylabel('Standard Deviation of Zinc Values')
plt.title('Standard Deviation of Zinc Values by Food Group (Descending Order)')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# Calculate median absolute deviation of zinc values by food group
zinc_mad = df_zinc.groupby('Food Group')['Zinc Value'].apply(lambda x: x.median() - x.mean())
print(f"Median Absolute Deviation of Zinc Values by Food Group:\n{zinc_mad}")

# Create a new DataFrame with median absolute deviations
zinc_mad_df = zinc_mad.to_frame('Median Absolute Deviation of Zinc Values').reset_index()
print(f"Median Absolute Deviation of Zinc Values DataFrame Shape:\n{zinc_mad_df.shape}")
print(f"Median Absolute Deviation of Zinc Values DataFrame Column Names:\n{zinc_mad_df.columns.tolist()}")
print(f"Median Absolute Deviation of Zinc Values DataFrame Types:\n{zinc_mad_df.dtypes}")
print(f"First few rows of Median Absolute Deviation of Zinc Values DataFrame:\n{zinc_mad_df.head()}")

# Plot median absolute deviations of zinc values by food group in descending order
zinc_mad_df_copy = zinc_mad_df.copy()
zinc_mad_df_copy = zinc_mad_df_copy.sort_values(by='Median Absolute Deviation of Zinc Values', ascending=False)
plt.figure(figsize=(10,6))
plt.bar(zinc_mad_df_copy['Food Group'], zinc_mad_df_copy['Median Absolute Deviation of Zinc Values'])
plt.xlabel('Food Group')
plt.ylabel('Median Absolute Deviation of Zinc Values')
plt.title('Median Absolute Deviation of Zinc Values by Food Group (Descending Order)')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# Calculate interquartile range of zinc values by food group
zinc_iqr = df_zinc.groupby('Food Group')['Zinc Value'].apply(lambda x: x.quantile(0.75) - x.quantile(0.25))
print(f"Interquartile Range of Zinc Values by Food Group:\n{zinc_iqr}")

# Create a new DataFrame with interquartile ranges
zinc_iqr_df = zinc_iqr.to_frame('Interquartile Range of Zinc Values').reset_index()
print(f"Interquartile Range of Zinc Values DataFrame Shape:\n{zinc_iqr_df.shape}")
print(f"Interquartile Range of Zinc Values DataFrame Column Names:\n{zinc_iqr_df.columns.tolist()}")
print(f"Interquartile Range of Zinc Values DataFrame Types:\n{zinc_iqr_df.dtypes}")
print(f"First few rows of Interquartile Range of Zinc Values DataFrame:\n{zinc_iqr_df.head()}")

# Plot interquartile ranges of zinc values by food group in descending order
zinc_iqr_df_copy = zinc_iqr_df.copy()
zinc_iqr_df_copy = zinc_iqr_df_copy.sort_values(by='Interquartile Range of Zinc Values', ascending=False)
plt.figure(figsize=(10,6))
plt.bar(zinc_iqr_df_copy['Food Group'], zinc_iqr_df_copy['Interquartile Range of Zinc Values'])
plt.xlabel('Food Group')
plt.ylabel('Interquartile Range of Zinc Values')
plt.title('Interquartile Range of Zinc Values by Food Group (Descending Order)')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# Calculate coefficient of variation of zinc values by food group
zinc_cv = df_zinc.groupby('Food Group')['Zinc Value'].apply(lambda x: x.std() / x.mean())
print(f"Coefficient of Variation of Zinc Values by Food Group:\n{zinc_cv}")

# Create a new DataFrame with coefficients of variation
zinc_cv_df = zinc_cv.to_frame('Coefficient of Variation of Zinc Values').reset_index()
print(f"Coefficient of Variation of Zinc Values DataFrame Shape:\n{zinc_cv_df.shape}")
print(f"Coefficient of Variation of Zinc Values DataFrame Column Names:\n{zinc_cv_df.columns.tolist()}")
print(f"Coefficient of Variation of Zinc Values DataFrame Types:\n{zinc_cv_df.dtypes}")
print(f"First few rows of Coefficient of Variation of Zinc Values DataFrame:\n{zinc_cv_df.head()}")

# Plot coefficients of variation of zinc values by food group in descending order
zinc_cv_df_copy = zinc_cv_df.copy()
zinc_cv_df_copy = zinc_cv_df_copy.sort_values(by='Coefficient of Variation of Zinc Values', ascending=False)
plt.figure(figsize=(10,6))
plt.bar(zinc_cv_df_copy['Food Group'], zinc_cv_df_copy['Coefficient of Variation of Zinc Values'])
plt.xlabel('Food Group')
plt.ylabel('Coefficient of Variation of Zinc Values')
plt.title('Coefficient of Variation of Zinc Values by Food Group (Descending Order)')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()