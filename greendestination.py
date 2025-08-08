#libraries used
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#data loading and cleaning
df = pd.read_csv("greendestination.csv")

#Ensure Attrition column is treated as ordered categorical
df['Attrition'] = pd.Categorical(df['Attrition'], categories=['No', 'Yes'], ordered=True)

# Basic inspection
df.info()
df.describe()
df.isnull().sum()

# Drop duplicates if any
df.drop_duplicates(inplace=True)


# Calculate the counts for 'Yes' and 'No' attrition.
attrition_counts = df['Attrition'].value_counts()
labels = ['No', 'Yes']

# TOTAL ATTRITION
plt.figure(figsize=(8, 8))
plt.pie(attrition_counts, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#5DADE2', '#E74C3C'])
plt.title('Overall Employee Attrition Rate', fontsize=16)
plt.show()

# Create a figure with two subplots for the box plots to help with the upcoming visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# ATTRITION VS AGE
sns.boxplot(x='Attrition', y='Age', data=df, ax=ax1, palette='pastel')
ax1.set_title('Age Distribution by Attrition')
ax1.set_xlabel('Attrition')
ax1.set_ylabel('Age')

# ATTRITION VS YEARS AT COMPANY
sns.boxplot(x='Attrition', y='YearsAtCompany', data=df, ax=ax2, palette='pastel')
ax2.set_title('Years at Company Distribution by Attrition')
ax2.set_xlabel('Attrition')
ax2.set_ylabel('Years at Company')

plt.tight_layout()
plt.show()

#ATTRITION VS GENDER
#filters only those who left the company
left_df = df[df['Attrition'] == 'Yes'] 

# Plot
sns.countplot(x='Gender', data=left_df, palette='Set2')
plt.title('Attrition by Gender')
plt.ylabel('Number of Employees Who Left')
plt.xlabel('Gender')
plt.show()


#ATTRITION VS INCOME
#helps us identify whether lower income employees are more likely to leave

# Create income bins
df['Income_Category'] = pd.qcut(df['MonthlyIncome'], 4, labels=['Lowest', 'Low', 'High', 'Highest']) 

# Calculate the attrition rate per income category
attrition_by_income = df.groupby('Income_Category')['Attrition'].apply(lambda x: (x == 'Yes').sum() / len(x))
attrition_by_income = attrition_by_income.reset_index(name='AttritionRate') 

# Create a bar chart.
plt.figure(figsize=(10, 6))
sns.barplot(x='Income_Category', y='AttritionRate', data=attrition_by_income, palette='viridis')
plt.title('Attrition Rate by Monthly Income Quartile')
plt.xlabel('Monthly Income Quartile')
plt.ylabel('Attrition Rate')
plt.show()