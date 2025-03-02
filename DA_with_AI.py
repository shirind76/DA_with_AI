import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("WVS_subset.csv")

# Define relevant columns
gender_col = "Q260"  # Gender: 1 = Male, 2 = Female, -2/-5 = No Data
education_col = "Q275"  # Education level
social_attitudes_cols = {
    "Q57": "Most people can be trusted?",
    "Q69": "How much confidence do you have in the police?",
    "Q86": "How much confidence do you have in NATO?",
    "Q265": "Is your father an immigrant?",
    "Q87": "How much confidence do you have in the World Bank?",
    "Q12": "Is tolerance and respect an important child quality?",
    "Q10": "Is a feeling of responsibility an important child quality?",
    "Q30": "Is university more important for boys than for girls?",
    "Q29": "Do men make better political leaders than women?",
    "Q33": "Should men have more right to a job than women when jobs are scarce?",
    "Q36": "Are homosexual couples as good parents as other couples?",
    "Q88": "How much confidence do you have in the WHO?",
    "Q288": "What is your income level?"
}

# Convert gender to readable categories, including missing values
df[gender_col] = df[gender_col].replace({1: "Male", 2: "Female", -2: "No Data", -5: "No Data" , -1:"No Data", -4:"No Data"})

# Create education categories and handle missing values
edu_mapping = {
    0: "No Education", 1: "Primary", 2: "Lower Secondary", 3: "Upper Secondary", 4: "Post-Secondary",
    5: "Short-cycle Tertiary", 6: "Bachelor", 7: "Master", 8: "Doctoral"
}
df[education_col] = df[education_col].map(edu_mapping)
df[education_col] = df[education_col].fillna("Unknown")  # Handle missing values

# Response label mappings for all social attitude questions
response_labels = {
    "Q57": {1: "Most people can be trusted", 2: "Need to be very careful", -1: "Don’t know", -2: "No answer", -4: "Not asked", -5: "Missing"},
    "Q69": {1: "A great deal", 2: "Quite a lot", 3: "Not very much", 4: "None at all"},
    "Q86": {1: "A great deal", 2: "Quite a lot", 3: "Not very much", 4: "None at all"},
    "Q265": {1: "Yes", 2: "No"},
    "Q87": {1: "A great deal", 2: "Quite a lot", 3: "Not very much", 4: "None at all"},
    "Q12": {1: "Yes", 2: "No"},
    "Q10": {1: "Yes", 2: "No"},
    "Q30": {1: "Yes", 2: "No"},
    "Q29": {1: "Yes", 2: "No"},
    "Q33": {1: "Men should have more right to a job", 2: "Equal rights for men and women"},
    "Q36": {1: "Yes", 2: "No"},
    "Q88": {1: "A great deal", 2: "Quite a lot", 3: "Not very much", 4: "None at all"},
    "Q288": {1: "Low income", 2: "Middle income", 3: "High income"}
}

# Function to filter out invalid responses and create horizontal bar plots
def plot_social_attitudes_by_group(df, col, group_by, title):
    plt.figure(figsize=(12, 6))
    
    # Remove invalid responses (e.g., missing codes)
    filtered_df = df[df[col] >= 0]
    
    # Replace numeric responses with meaningful labels if available
    if col in response_labels:
        filtered_df[col] = filtered_df[col].map(response_labels[col])
    
    # Calculate percentage distribution
    grouped_data = filtered_df.groupby([group_by, col]).size().unstack()
    percentage_data = grouped_data.div(grouped_data.sum(axis=1), axis=0) * 100
    
    # Plot horizontal stacked bar chart
    ax = percentage_data.plot(kind='barh', stacked=True, colormap='RdYlGn', figsize=(12, 6))
    plt.xlabel("Percentage")
    plt.ylabel("Gender" if group_by == gender_col else "Education Level")
    plt.title(title)
    plt.legend(title="Response", loc='upper right', bbox_to_anchor=(1.3, 1))
    
    # Display value labels inside bars
    for bars in ax.containers:
        ax.bar_label(bars, fmt='%.1f%%', label_type='center', fontsize=8, color='black')
    
    plt.show()

# Visualizing social attitudes by gender
def visualize_by_gender():
    for col, question in social_attitudes_cols.items():
        plot_social_attitudes_by_group(df, col, gender_col, f"{question} by Gender")

# Visualizing social attitudes by education
def visualize_by_education():
    for col, question in social_attitudes_cols.items():
        plot_social_attitudes_by_group(df, col, education_col, f"{question} by Education Level")

# Run the visualization functions
visualize_by_gender()
visualize_by_education()

# Select the five most important variables for descriptive statistics
selected_columns = {
    "Q57": "Most people can be trusted",
    "Q69": "Confidence in the police",
    "Q86": "Confidence in NATO",
    "Q87": "Confidence in the World Bank",
    "Q33": "Job Gender Inequality"
}

# Compute descriptive statistics
descriptive_stats = df[list(selected_columns.keys())].describe().T  # Transpose for better readability

# Rename index to reflect question topics
descriptive_stats.index = descriptive_stats.index.map(selected_columns)

# Keep only the required statistics
descriptive_stats = descriptive_stats[['count', 'mean', 'std', 'min', '50%', 'max']]

# Rename columns for a structured table
descriptive_stats = descriptive_stats.rename(columns={
    "count": "N",
    "mean": "Mean",
    "std": "Standard Deviation",
    "min": "Minimum",
    "50%": "Median",
    "max": "Maximum"
})

# Round values for clarity
descriptive_stats = descriptive_stats.round(3)

# Add "Variable" as the first column header
descriptive_stats.insert(0, "Variable", descriptive_stats.index)

# Create a well-formatted table visualization
fig, ax = plt.subplots(figsize=(15, 6))  # Adjust figure size for readability
ax.axis('tight')
ax.axis('off')

# Define alternating row colors
row_colors = [['#f0f0f0' if i % 2 == 0 else '#ffffff' for _ in range(len(descriptive_stats.columns))] 
              for i in range(len(descriptive_stats))]

# Create the table with evenly spaced columns
table = ax.table(cellText=descriptive_stats.values,
                 colLabels=descriptive_stats.columns,
                 cellLoc='center',
                 loc='center',
                 cellColours=row_colors,
                 bbox=[0, 0, 1.5,1])  # Adjust table size

# Set table style
table.auto_set_font_size(False)
table.set_fontsize(12)

for i in range(num_cols):
    table[(0, i)].set_width( 1/num_cols)  # Apply uniform width to all columns

# Format header row
for i in range(num_cols):
    cell = table[0, i]  # Header row starts at (0, i)
    cell.set_text_props(weight='bold', fontsize=14, color='white')
    cell.set_facecolor('#4c72b0')  # Dark blue header

# Title formatting
plt.title("Summary of Descriptive Statistics", fontsize=20, fontweight="bold", loc='right', pad=30)

# Show the table
plt.show()
