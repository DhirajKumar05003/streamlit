import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv("projext (1).csv")

# Function to convert "Yes" and "No" to binary
def to_binary(d):
    return 1 if d == "Yes" else 0

# Rename columns
newnames = ["Timestamps", "Names", "Gender", "Age", "Major", "Year", "CGPA", "Married", "Depression", "Anxiety", "Panic Attacks", "Treated"]
df.columns = newnames

# Convert categorical columns to binary
df["Married"] = df["Married"].apply(to_binary)
df["Depression"] = df["Depression"].apply(to_binary)
df["Anxiety"] = df["Anxiety"].apply(to_binary)
df["Panic Attacks"] = df["Panic Attacks"].apply(to_binary)
df["Treated"] = df["Treated"].apply(to_binary)
df["Year"] = df["Year"].str[-1:]

# Add "Condition" column
has_smtn = [(1 if df.iloc[row, df.columns.get_loc("Depression")] == 1 or
                 df.iloc[row, df.columns.get_loc("Anxiety")] == 1 or
                 df.iloc[row, df.columns.get_loc("Panic Attacks")] == 1 else 0) for row in range(len(df.index))]
df["Condition"] = has_smtn

# Main menu
while True:
    st.sidebar.title("Menu")
    choice = st.sidebar.radio("Select an option", ["Display the dataset", "Display dataset with new column names",
                                                   "Display count of missing values", "Convert categorical columns to binary",
                                                   "Display dataset after adding 'Condition' column", "Display statistics",
                                                   "Display condition by gender plot"])

    if choice == "Display the dataset":
        st.write(df)
    elif choice == "Display dataset with new column names":
        st.write(df.rename(columns=newnames))
    elif choice == "Display count of missing values":
        st.write(df.isna().sum())
    elif choice == "Convert categorical columns to binary":
        st.write("Columns converted to binary and Year column updated.")
    elif choice == "Display dataset after adding 'Condition' column":
        st.write(df)
    elif choice == "Display statistics":
        if "Depression" in df.columns and "Anxiety" in df.columns and "Panic Attacks" in df.columns:
            num_depressed = (df["Depression"] == 1).sum()
            num_anxious = (df["Anxiety"] == 1).sum()
            num_pa = (df["Panic Attacks"] == 1).sum()
            num_treated = (df["Treated"] == 1).sum()
            num_w_condition = (df["Condition"] == 1).sum()
            num_wo_condition = (df["Condition"] == 0).sum()
            st.write("Depressed: {}\nAnxious: {}\nHaving panic attacks: {}\nBeing treated: {}\nTotal people with a condition: {}\nTotal people without: {}"
                     .format(num_depressed, num_anxious, num_pa, num_treated, num_w_condition, num_wo_condition))
        else:
            st.write("Depression, Anxiety, or Panic Attacks columns not found in the DataFrame.")
    elif choice == "Display condition by gender plot":
        if "Depression" in df.columns and "Anxiety" in df.columns and "Panic Attacks" in df.columns and "Gender" in df.columns:
            labels = ['Depressed', 'Anxious', 'Having Panic \nAttacks',
                      'Depressed and \nAnxious', 'Depressed and Having \nPanic Attacks',
                      'Anxious and Having \nPanic Attacks', 'All Three']

            gender_counts = {
                "Male": [(df[(df["Gender"] == "Male") & (df["Depression"] == 1)].shape[0]),
                         (df[(df["Gender"] == "Male") & (df["Anxiety"] == 1)].shape[0]),
                         (df[(df["Gender"] == "Male") & (df["Panic Attacks"] == 1)].shape[0]),
                         (df[(df["Gender"] == "Male") & (df["Depression"] == 1) & (df["Anxiety"] == 0) & (df["Panic Attacks"] == 0)].shape[0]),
                         (df[(df["Gender"] == "Male") & (df["Depression"] == 1) & (df["Anxiety"] == 0) & (df["Panic Attacks"] == 0)].shape[0]),
                         (df[(df["Gender"] == "Male") & (df["Anxiety"] == 1) & (df["Depression"] == 0) & (df["Panic Attacks"] == 0)].shape[0]),
                         (df[(df["Gender"] == "Male") & (df["Depression"] == 1) & (df["Anxiety"] == 1) & (df["Panic Attacks"] == 1)].shape[0])],

                "Female": [(df[(df["Gender"] == "Female") & (df["Depression"] == 1)].shape[0]),
                           (df[(df["Gender"] == "Female") & (df["Anxiety"] == 1)].shape[0]),
                           (df[(df["Gender"] == "Female") & (df["Panic Attacks"] == 1)].shape[0]),
                           (df[(df["Gender"] == "Female") & (df["Depression"] == 1) & (df["Anxiety"] == 0) & (df["Panic Attacks"] == 0)].shape[0]),
                           (df[(df["Gender"] == "Female") & (df["Depression"] == 1) & (df["Anxiety"] == 0) & (df["Panic Attacks"] == 0)].shape[0]),
                           (df[(df["Gender"] == "Female") & (df["Anxiety"] == 1) & (df["Depression"] == 0) & (df["Panic Attacks"] == 0)].shape[0]),
                           (df[(df["Gender"] == "Female") & (df["Depression"] == 1) & (df["Anxiety"] == 1) & (df["Panic Attacks"] == 1)].shape[0])]
            }

            gender_counts["Male"] = np.array(gender_counts["Male"]) / (df["Gender"] == "Male").sum() * 100
            gender_counts["Female"] = np.array(gender_counts["Female"]) / (df["Gender"] == "Female").sum() * 100

            fig, ax = plt.subplots(figsize=(10, 3))
            bottom = np.zeros(7)

            for gender, gender_count in gender_counts.items():
                p = ax.bar(labels,
                           gender_count,
                           width=0.8,
                           label=gender,
                           bottom=bottom)
                bottom += gender_count
                ax.bar_label(container=p,
                             label_type='center',
                             fontsize=10)

            ax.set_title("Condition by Gender", fontsize=20)
            plt.xticks(fontsize=8, ha='right', rotation=20)
            ax.legend()
            st.pyplot(fig)
        else:
            st.write("Depression, Anxiety, Panic Attacks, or Gender columns not found in the DataFrame.")

# Main menu
while True:
    st.sidebar.title("Menu")
    choice = st.sidebar.radio("Select an option", ["Display the dataset", "Display dataset with new column names",
                                                   "Display count of missing values", "Convert categorical columns to binary",
                                                   "Display dataset after adding 'Condition' column", "Display statistics",
                                                   "Display condition by gender plot"])

    if choice == "Display the dataset":
        st.write(df)
    elif choice == "Display dataset with new column names":
        st.write(df.rename(columns=newnames))
    # Add similar blocks for other options...

    # Include a break condition to exit the loop
    if choice == "Exit":
        break
