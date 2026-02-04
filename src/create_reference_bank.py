import pandas as pd
import json

# Load dataset
df = pd.read_csv("../data/refstdcombined.csv")

# Group by question and take the first reference answer for each
reference_bank = {}

grouped = df.groupby("QuestionID")

for q_id, group in grouped:
    ref_answer = group["ReferenceAnswer"].iloc[0]
    reference_bank[q_id] = [ref_answer]   # store as a list (we will add more later)

# Save to JSON file
with open("../data/reference_bank.json", "w") as f:
    json.dump(reference_bank, f, indent=4)

print("Reference bank created successfully!")
