import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

file_path = "WVS_subset.csv"
df = pd.read_csv(file_path)

gender_col = "Q260"  
education_col = "Q275"  
social_attitudes_cols = {
    "Q57": "Most people can be trusted?",
    "Q69": "How much confidence do you have in the police?",
    "Q86": "How much confidence do you have in NATO?",
    "Q265": "Is your father an immigrant?",
    "Q87": "How much confidence do you have in the World Bank?",
    "Q12": "Is tolerance and respect an important child quality?",
    "Q30": "Is university more important for boys than for girls?",
    "Q29": "Do men make better political leaders than women?",
    "Q33": "Should men have more right to a job than women when jobs are scarce?",
    "Q36": "Are homosexual couples as good parents as other couples?"
}

# Convert gender to readable categories, including missing values
df[gender_col] = df[gender_col].replace({1: "Male", 2: "Female", -2: "No Data", -5: "No Data", -1: "No Data", -4: "No Data"})

# Create education categories and handle missing values
edu_mapping = {
    0: "No Education", 1: "Primary", 2: "Lower Secondary", 3: "Upper Secondary",
    4: "Post-Secondary", 5: "Short-cycle Tertiary", 6: "Bachelor",
    7: "Master", 8: "Doctoral"
}
df[education_col] = df[education_col].map(edu_mapping).fillna("Unknown")  # Handle missing values

output_dir = "figures"
os.makedirs(output_dir, exist_ok=True)

# Response label mappings for social attitude questions
response_labels = {
    "Q57": {1: "Most people can be trusted", 2: "Need to be very careful"},
    "Q69": {1: "A great deal", 2: "Quite a lot", 3: "Not very much", 4: "None at all"},
    "Q86": {1: "A great deal", 2: "Quite a lot", 3: "Not very much", 4: "None at all"},
    "Q265": {1: "Yes", 2: "No"},
    "Q87": {1: "A great deal", 2: "Quite a lot", 3: "Not very much", 4: "None at all"},
    "Q12": {1: "Yes", 2: "No"},
    "Q30": {1: "Agree", 2: "Disagree"},
    "Q29": {1: "Agree", 2: "Disagree"},
    "Q33": {1: "Men should have more right to a job", 2: "Equal rights for men and women"},
    "Q36": {1: "Yes", 2: "No"}
}

# Function to filter out invalid responses and create horizontal bar plots
def plot_social_attitudes_by_group(df, col, group_by, title, file_name):
    plt.figure(figsize=(12, 6))
    
    filtered_df = df[df[col].isin(response_labels.get(col, {}).keys())]
    
    if col in response_labels:
        filtered_df[col] = filtered_df[col].map(response_labels[col])
    
    grouped_data = filtered_df.groupby([group_by, col]).size().unstack()
    percentage_data = grouped_data.div(grouped_data.sum(axis=1), axis=0) * 100

    ax = percentage_data.plot(kind='barh', stacked=True, colormap='RdYlGn', figsize=(12, 6))
    plt.xlabel("Percentage")
    plt.ylabel("Gender" if group_by == gender_col else "Education Level")
    plt.title(title)
    plt.legend(title="Response", loc='upper right', bbox_to_anchor=(1.3, 1))


    plt.savefig(os.path.join(output_dir, file_name), bbox_inches='tight')
    plt.close()

# Generate and save all visualizations
for col, question in social_attitudes_cols.items():
    plot_social_attitudes_by_group(df, col, gender_col, f"{question} by Gender", f"{col}_by_gender.png")

    plot_social_attitudes_by_group(df, col, education_col, f"{question} by Education Level", f"{col}_by_education.png")

print("All figures have been generated and saved successfully.")

selected_variables = ["Q57", "Q69", "Q86", "Q265", "Q87", "Q12", "Q30", "Q29", "Q33", "Q36"]

# Compute descriptive statistics
descriptive_stats = df[selected_variables].describe().T

descriptive_stats = descriptive_stats[['count', 'mean', 'std', 'min', '50%', 'max']]
descriptive_stats.columns = ['N', 'Mean', 'Std. Dev.', 'Min', 'Median', 'Max']
descriptive_stats = descriptive_stats.round(2)
print(descriptive_stats)