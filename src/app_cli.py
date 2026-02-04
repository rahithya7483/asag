import json
from final_grader import grade_student_answer
from load_questions import get_question_text
# Load reference bank to show valid Question IDs
reference_bank = json.load(open("../data/multi_reference_bank.json"))


def list_questions():
    print("\nAvailable Questions:")
    for qid in reference_bank.keys():
        question_text = get_question_text(qid)
        print(f"\n{qid}:")
        print("   ", question_text)


def main():
    print("\n=== Automatic Short Answer Grading System ===")

    while True:

        list_questions()

        question_id = input("\nEnter Question ID (or type 'exit'): ").strip()

        if question_id.lower() == "exit":
            print("Thank you. Exiting...")
            break

        if question_id not in reference_bank:
            print("Invalid Question ID! Try again.\n")
            continue

        # Show actual question
        print("\nQuestion:", get_question_text(question_id))

        student_answer = input("\nEnter your answer: ")

        print("\nEvaluating...\n")

        result = grade_student_answer(question_id, student_answer)

        print("=== RESULT ===")
        print("Similarity Score:", result["similarity_score"])
        print("Percentage Match:", result["percent_match"])
        print("Matched Concepts:", result["matched_concepts"])
        print("Missing Concepts:", result["missing_concepts"])
        print("Feedback:", result["final_feedback"])

        # Show correct answer(s) only if not excellent
        if result["percent_match"] < 90:
            print("\nCorrect Reference Answer(s):")
            for idx, ref in enumerate(reference_bank[question_id], start=1):
                print(f"{idx}. {ref}")

        print("\n============================\n")

        again = input("Do you want to test another answer? (yes/no): ").strip().lower()

        if again != "yes":
            print("\nThank you for using the ASAG System!")
            break

        print("\n----------------------------------------\n")

if __name__ == "__main__":
    main()
