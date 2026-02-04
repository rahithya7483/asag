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


def random_swap(sentence):
    words = sentence.split()
    if len(words) < 2:
        return sentence

    i, j = random.sample(range(len(words)), 2)
    words[i], words[j] = words[j], words[i]
    return " ".join(words)


def augment_reference_answer(answer):
    augmented = set()
    augmented.add(answer)
    augmented.add(synonym_replacement(answer))
    augmented.add(random_swap(answer))
    return list(augmented)
