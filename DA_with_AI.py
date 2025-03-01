import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = "WVS_subset.csv"  # Adjust path if needed
df = pd.read_csv(file_path)

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
df[gender_col] = df[gender_col].replace({1: "Male", 2: "Female", -2: "No Data", -5: "No Data"})

# Create education categories and handle missing values
edu_mapping = {
    0: "No Education", 1: "Primary", 2: "Lower Secondary", 3: "Upper Secondary", 4: "Post-Secondary",
    5: "Short-cycle Tertiary", 6: "Bachelor", 7: "Master", 8: "Doctoral"
}
df[education_col] = df[education_col].map(edu_mapping)
df[education_col] = df[education_col].fillna("Unknown")  # Handle missing values

# Ensure Gender_Education column is properly created by converting gender_col to string
df["Gender_Education"] = df[gender_col].astype(str) + " - " + df[education_col].astype(str)

# Drop rows where Gender_Education is missing
df = df.dropna(subset=["Gender_Education"])

# Function to filter out invalid responses and create horizontal bar plots
def plot_social_attitudes_by_group(df, col, group_by, title):
    plt.figure(figsize=(12, 6))
    
    # Remove invalid responses (e.g., negative values or missing codes)
    filtered_df = df[df[col] >= 0]
    
    # Calculate percentage distribution
    grouped_data = filtered_df.groupby([group_by, col]).size().unstack()
    percentage_data = grouped_data.div(grouped_data.sum(axis=1), axis=0) * 100
    
    # Plot horizontal stacked bar chart
    ax = percentage_data.plot(kind='barh', stacked=True, colormap='RdYlGn', figsize=(12, 6))
    plt.xlabel("Percentage")
    plt.ylabel(group_by)
    plt.title(title)
    plt.legend(title="Response", loc='upper right', bbox_to_anchor=(1.3, 1))
    
    # Display value labels inside bars
    for bars in ax.containers:
        ax.bar_label(bars, fmt='%.1f%%', label_type='center', fontsize=8, color='black')
    
    plt.show()

# Visualizing social attitudes by combined Gender and Education
def visualize_combined():
    for col, question in social_attitudes_cols.items():
        plot_social_attitudes_by_group(df, col, "Gender_Education", f"{question} by Gender and Education")

# Run the visualization function
visualize_combined()
