import pandas as pd

# Load real Kaggle dataset
df = pd.read_csv("Students.csv")

# See what we have
print("Original columns:", df.columns.tolist())
print("Shape:", df.shape)

# Rename columns to simpler names
df = df.rename(columns={
    "math score": "math",
    "reading score": "reading",
    "writing score": "writing"
})

# Create pass_fail column (average >= 40 = Pass)
df["average"] = (df["math"] + df["reading"] + df["writing"]) / 3
df["pass_fail"] = (df["average"] >= 40).astype(int)

# Check pass/fail distribution
print("\nPass/Fail counts:")
print(df["pass_fail"].value_counts())

# Save cleaned version
df.to_csv("students_clean.csv", index=False)
print("\nCleaned data saved as students_clean.csv ✅")
print(df.head())