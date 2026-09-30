"""Compare the grader's similarity scores with human scores.

Run from inside src/:  python evaluate_correlation.py

Reports Pearson and Spearman correlation between the model's max cosine
similarity and the human average score (0-5), for:
  - the single-reference bank (reference_bank_cleaned.json)
  - the augmented multi-reference bank (multi_reference_bank.json)
"""
import json

import pandas as pd
from scipy.stats import pearsonr, spearmanr
from sentence_transformers import util

from evaluate_answer import model  # same SBERT model used by the grader

DATA = "../data/"

single_bank = json.load(open(DATA + "reference_bank_cleaned.json"))
multi_bank = json.load(open(DATA + "multi_reference_bank.json"))

df = pd.read_csv(DATA + "refstdcombined.csv", encoding_errors="replace")
df = df[df["QuestionID"].isin(multi_bank)]
df = df.dropna(subset=["StudentAnswer", "avg_score"]).reset_index(drop=True)
df["StudentAnswer"] = df["StudentAnswer"].astype(str)

print(f"Evaluating {len(df)} human-graded answers...")
student_embs = model.encode(
    df["StudentAnswer"].tolist(), convert_to_tensor=True, batch_size=64, show_progress_bar=True
)


def max_similarities(bank):
    ref_embs = {q: model.encode(refs, convert_to_tensor=True) for q, refs in bank.items()}
    sims = []
    for i, qid in enumerate(df["QuestionID"]):
        sims.append(float(util.cos_sim(student_embs[i], ref_embs[qid]).max()))
    return pd.Series(sims)


def report(name, sims):
    human = df["avg_score"]
    print(f"\n{name}")
    print(f"  Pearson  r   = {pearsonr(sims, human)[0]:.3f}")
    print(f"  Spearman rho = {spearmanr(sims, human)[0]:.3f}")
    for subject in ["PythonQ", "BasicML"]:
        mask = df["QuestionID"].str.startswith(subject)
        rho = spearmanr(sims[mask], human[mask])[0]
        print(f"  {subject:8s} Spearman rho = {rho:.3f}  (n={mask.sum()})")


report("Single reference", max_similarities(single_bank))
report("Multi-reference + augmentation", max_similarities(multi_bank))
