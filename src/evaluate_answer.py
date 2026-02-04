from sentence_transformers import SentenceTransformer, util
import json

# 1. Load SBERT model (one of the best)
model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

# 2. Load cleaned reference bank
reference_bank = json.load(open("../data/multi_reference_bank.json"))

def evaluate_answer(question_id, student_answer):
    """
    Compute semantic similarity between student answer and all correct reference answers.
    Returns: percent score, raw cosine similarity
    """
    # Get all correct answers for this question
    ref_answers = reference_bank.get(question_id, None)

    if ref_answers is None:
        return None, "Invalid Question ID"

    # 3. Encode student and references
    student_emb = model.encode(student_answer, convert_to_tensor=True)
    ref_embs = model.encode(ref_answers, convert_to_tensor=True)

    # 4. Compute similarity scores
    similarities = util.cos_sim(student_emb, ref_embs)[0]

    # 5. Take maximum similarity
    max_sim = float(similarities.max().item())

    # 6. Convert cosine similarity (-1 to 1) → percent (0 to 100)
    percent_score = (max_sim + 1) / 2 * 100

    return percent_score, max_sim

# Testing (temporary)
if __name__ == "__main__":
    qid = "PythonQ011"
    student = "Anonymous functions are made using lambda expression."

    score, sim = evaluate_answer(qid, student)
    print("Similarity Score:", sim)
    print("Percentage Match:", score)
