import streamlit as st
import json
from final_grader import grade_student_answer
from load_questions import get_question_text

# Load reference bank
reference_bank = json.load(open("../data/reference_bank_cleaned.json"))

st.title("Automatic Short Answer Grading System (ASAG)")
st.write("This tool evaluates student answers using semantic similarity and explainability.")

# Dropdown to select question
question_id = st.selectbox(
    "Select Question ID",
    options=list(reference_bank.keys())
)

# Display full question text
st.subheader("Question")
st.write(get_question_text(question_id))

# Input text area for student's answer
student_answer = st.text_area("Enter your answer here")

# Evaluate button
if st.button("Evaluate Answer"):

    if not student_answer.strip():
        st.warning("Please enter an answer before evaluating.")
    else:
        result = grade_student_answer(question_id, student_answer)

        st.subheader("Result")
        st.write("**Similarity Score:**", result["similarity_score"])
        st.write("**Percentage Match:**", result["percent_match"])

        st.write("**Matched Concepts:**", result["matched_concepts"])
        st.write("**Missing Concepts:**", result["missing_concepts"])

        st.subheader("Feedback")
        st.success(result["final_feedback"])

        # Show correct answers if student is not excellent
        if result["percent_match"] < 90:
            st.subheader("Correct Reference Answer(s)")
            for idx, ref in enumerate(reference_bank[question_id], start=1):
                st.write(f"{idx}. {ref}")
