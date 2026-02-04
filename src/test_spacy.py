import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp("Lambda functions are anonymous.")
print([token.lemma_ for token in doc])
