import random
import nltk
from nltk.corpus import wordnet

nltk.download("wordnet")
nltk.download("omw-1.4")

def synonym_replacement(sentence, n=1):
    words = sentence.split()
    new_words = words.copy()
    random.shuffle(words)

    replaced = 0
    for word in words:
        synsets = wordnet.synsets(word)
        if synsets:
            synonym = synsets[0].lemmas()[0].name()
            if synonym != word:
                new_words = [synonym if w == word else w for w in new_words]
                replaced += 1
        if replaced >= n:
            break

    return " ".join(new_words)


def word_reordering(sentence):
    words = sentence.split()

    if len(words) < 4:
        return sentence

    # pick a sub-sequence to shuffle
    start = random.randint(0, len(words) - 3)
    end = start + random.randint(2, min(5, len(words) - start))

    sub_part = words[start:end]
    random.shuffle(sub_part)

    new_words = words[:start] + sub_part + words[end:]

    return " ".join(new_words)

def minor_text_variation(sentence):
    words = sentence.split()

    # random lowercase/uppercase variation
    if random.random() < 0.3:
        words = [w.lower() for w in words]

    # randomly add filler words
    fillers = ["very", "basically", "actually", "simply"]
    if random.random() < 0.3:
        insert_pos = random.randint(0, len(words)-1)
        words.insert(insert_pos, random.choice(fillers))

    # randomly remove a word (small noise)
    if len(words) > 4 and random.random() < 0.3:
        del words[random.randint(0, len(words)-1)]

    return " ".join(words)

def augment_reference_answer(answer):
    augmented = set()

    augmented.add(answer)
    augmented.add(synonym_replacement(answer))
    augmented.add(word_reordering(answer))
    augmented.add(minor_text_variation(answer))

    return list(augmented)
