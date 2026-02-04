import json
import re

# load file
data = json.load(open("../data/reference_bank.json"))

cleaned = {}

# keep only keys that match valid pattern like "PythonQ001" or "BasicML003"
pattern = re.compile(r"^[A-Za-z]+ML\d+$|^PythonQ\d+$")

for key, value in data.items():
    if isinstance(key, str) and pattern.match(key):
        cleaned[key] = value

# save cleaned version
with open("../data/reference_bank_cleaned.json", "w") as f:
    json.dump(cleaned, f, indent=4)

print("Cleaned reference bank created successfully!")
print("Total valid questions:", len(cleaned))
