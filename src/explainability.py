import spacy
import json

nlp = spacy.load("en_core_web_sm")

# Load cleaned reference bank
reference_bank = json.load(open("../data/multi_reference_bank.json"))

def extract_keywords(text):
    doc = nlp(text)
    keywords = []
    for token in doc:
        if token.pos_ in ["NOUN", "VERB", "ADJ"]:
            keywords.append(token.lemma_.lower())
    return keywords

def explain_answer(question_id, student_answer):
    if question_id not in reference_bank:
        return None

    reference_answers = reference_bank[question_id]

    # Combine all reference answers into one text block
    ref_text = " ".join(reference_answers)

    # Extract keywords
    ref_keywords = set(extract_keywords(ref_text))
    stud_keywords = set(extract_keywords(student_answer))

    # Compare concepts
    matched = list(ref_keywords.intersection(stud_keywords))
    missing = list(ref_keywords - stud_keywords)

    return {
        "matched_concepts": matched,
        "missing_concepts": missing
    }

# Testing temporarily
if __name__ == "__main__":
    qid = "PythonQ011"
    student = "Anonymous functions are made using lambda."

    result = explain_answer(qid, student)
    print(result)
