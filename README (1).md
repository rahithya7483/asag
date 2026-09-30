# Automatic Short Answer Grading (ASAG)

An NLP system that grades short technical answers by comparing them with
multiple reference answers using Sentence Transformers, and explains each
result by showing which key concepts the student covered and which were missing.

Covers **114 questions** (68 Python, 46 Basic Machine Learning) with a dataset of
about **4,000 student answers graded by two human graders** (0-5 scale).

## Features

- **Semantic scoring**: encodes the student answer and the reference answers with
  a Sentence Transformers model (`paraphrase-MiniLM-L6-v2`, 384-dim embeddings)
  and uses cosine similarity, so a correct answer worded differently still scores well.
- **Multi-reference matching**: each question has several reference answers, and
  the student answer is scored against the best match.
- **Reference-answer augmentation**: 5 human-written references per question are
  expanded to about 17 per question (1,900+ in total) using WordNet synonym
  replacement, word reordering, and light text noise (filler words, casing, word drops).
- **Explainable feedback**: spaCy extracts key nouns, verbs and adjectives (lemmatized)
  and reports matched and missing concepts alongside the score.
- **Two interfaces**: a terminal app and a Streamlit web app.

## How it works

```
Student answer
   -> SBERT encoding (384-dim vector)
   -> cosine similarity with every reference vector
   -> take the maximum similarity
   -> convert to a percentage and a feedback band
   -> spaCy keyword comparison -> matched / missing concepts
```

Feedback bands: 90%+ excellent, 70-89% good, 50-69% partially correct, below 50% incorrect.

## Project structure

```
asag/
├── data/
│   ├── Question_data.csv                 # 114 questions (ID, text, type)
│   ├── refstdcombined.csv                # ~4,000 student answers with human scores
│   ├── multiple_reference_answers.xlsx   # 5 reference answers per question
│   ├── reference_bank.json               # first-pass single-reference bank
│   ├── reference_bank_cleaned.json       # cleaned to the 114 valid question IDs
│   └── multi_reference_bank.json         # augmented references used for grading
└── src/
    ├── create_reference_bank.py          # builds the single-reference bank from the CSV
    ├── clean_reference_bank.py           # keeps only valid question IDs
    ├── augmentation_utils.py             # synonym replacement, reordering, noise
    ├── multi_reference.py                # builds the augmented multi-reference bank
    ├── evaluate_answer.py                # SBERT similarity scoring
    ├── explainability.py                 # spaCy matched / missing concepts
    ├── final_grader.py                   # combines score, concepts and feedback
    ├── load_questions.py                 # question ID -> question text
    ├── app_cli.py                        # terminal interface
    ├── streamlit_app.py                  # web interface
    └── evaluate_correlation.py           # compares scores with human grades
```

## Setup

```bash
pip install sentence-transformers spacy pandas openpyxl nltk streamlit scipy
python -m spacy download en_core_web_sm
```

All scripts use relative paths, so run them from inside the `src/` folder.

```bash
cd src

# optional: rebuild the reference banks (the built files are already in data/)
python create_reference_bank.py
python clean_reference_bank.py
python multi_reference.py

# run the grader
python app_cli.py                # terminal
streamlit run streamlit_app.py   # web UI
```

## Example

Choose a question ID (for example `PythonQ011`), type an answer, and the app returns:

- the similarity score and percentage match
- matched concepts and missing concepts
- a feedback message
- the reference answers, if the score is below 90%

## Evaluation

`src/evaluate_correlation.py` scores every human-graded answer and reports the
correlation between the system's similarity and the human scores, for both the
single-reference and augmented multi-reference banks.

```bash
cd src
python evaluate_correlation.py
```

Results: `[add Pearson / Spearman values and N after running]`

## Limitations

- **Score mapping is coarse.** Cosine similarity is converted with `(sim + 1) / 2`,
  so an unrelated answer with similarity near 0 still maps to about 50%.
  The percentage bands should be calibrated against the human scores.
- **Concept matching is lexical.** Matched and missing concepts come from lemma
  overlap, so a correct paraphrase can show up as a missing concept.
- **Augmentation adds noise.** Word reordering and word drops can produce
  ungrammatical reference variants.
- **Small, domain-specific data.** Questions cover introductory Python and ML only.

## Future work

- Calibrate score bands against human grades (regression or thresholds tuned on the dataset)
- Semantic concept matching using embeddings instead of keyword overlap
- Compare other models (larger Sentence Transformers, cross-encoders) and fine-tune on the graded answers
- Use the Streamlit reference bank consistently and hide noisy augmented variants from students
