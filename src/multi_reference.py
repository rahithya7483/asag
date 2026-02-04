import pandas as pd
import json
from augmentation_utils import augment_reference_answer

# Load dataset (Excel or CSV)
df = pd.read_excel("../data/multiple_reference_answers.xlsx")
# If using CSV, uncomment below:
# df = pd.read_csv("../data/multiple_reference_answers.csv")

reference_bank = {}

# Group by QuestionID
grouped = df.groupby("QuestionID")

for q_id, group in grouped:
    expanded_answers = []

    # Convert Series → list of strings
    ref_answers = group["ReferenceAnswer"].astype(str).tolist()

    # Apply augmentation to each reference answer
    for ans in ref_answers:
        augmented_versions = augment_reference_answer(ans)
        expanded_answers.extend(augmented_versions)

    # Remove duplicate answers
    reference_bank[q_id] = list(set(expanded_answers))

# Save augmented multi-reference bank to JSON
with open("../data/multi_reference_bank.json", "w", encoding="utf-8") as f:
    json.dump(reference_bank, f, indent=4, ensure_ascii=False)

print("Multi-reference bank with augmentation created successfully!")
print("Total questions:", len(reference_bank))
