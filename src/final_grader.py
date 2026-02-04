from evaluate_answer import evaluate_answer
from explainability import explain_answer
import json

# Load reference bank (cleaned)
reference_bank = json.load(open("../data/multi_reference_bank.json"))

def grade_student_answer(question_id, student_answer):
    if question_id not in reference_bank:
        return {
            "error": "Invalid Question ID"
        }

    # 1. Compute similarity and percent
    percent, similarity = evaluate_answer(question_id, student_answer)

    # 2. Compute explainability (matched + missing concepts)
    explanation = explain_answer(question_id, student_answer)

    # 3. Build final output
    result = {
        "question_id": question_id,
        "student_answer": student_answer,
        "similarity_score": similarity,
        "percent_match": percent,
        "matched_concepts": explanation["matched_concepts"],
        "missing_concepts": explanation["missing_concepts"],
        "final_feedback": ""
    }

    # 4. Generate feedback based on score
    if percent >= 90:
        result["final_feedback"] = "Excellent answer. Fully correct."
    elif percent >= 70:
        result["final_feedback"] = "Good answer. Mostly correct but missing some details."
    elif percent >= 50:
        result["final_feedback"] = "Partially correct. Revise missing concepts."
    else:
        result["final_feedback"] = "Incorrect answer. Needs improvement."

    return result


# TESTING
if __name__ == "__main__":
    qid = "PythonQ011"
    student = "Anonymous functions are created using lambda."

    output = grade_student_answer(qid, student)
    print(json.dumps(output, indent=4))
