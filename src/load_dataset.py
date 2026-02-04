import pandas as pd

# Load the main dataset
df = pd.read_csv("../data/refstdcombined.csv")

print("Dataset loaded successfully!")
print("Number of rows:", len(df))
print("Columns:", df.columns)
print("\nFirst 5 rows:\n")
print(df.head())
