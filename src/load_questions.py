import pandas as pd

# Load CSV containing question text
question_df = pd.read_csv("../data/Question_data.csv")

# Convert to dictionary: {QuestionID: QuestionText}
question_dict = dict(zip(question_df["QuestionID"], question_df["QuestionText"]))

def get_question_text(qid):
    return question_dict.get(qid, "Question text not found")
