import re

from nltk import LancasterStemmer

stemmer = LancasterStemmer()


def get_all_reviewers(reviews):
    """
    collects all possible reviewers
    """
    reviewer_set = set()
    for review in reviews:
        for reviewer in review["reviewer_login"]:
            reviewer_set.add(reviewer)
    return list(reviewer_set)


def is_word_useful(word):
    """
    word filtering. removes digits and websites
    """
    for c in word:
        if c.isdigit():
            return False
    if "http://" in word or "https://" in word:
        return False
    return True


def word_stem(word):
    """
    removes punctuation and stems with LancasterStemmer
    """
    if word.endswith('.') or word.endswith(',') or word.endswith(':') or word.endswith('\'') or word.endswith('\"'):
        word = word[:-1]
    if word.startswith(',') or word.startswith('.') or word.startswith(':') or word.startswith('\'') or word.startswith(
            '\"'):
        word = word[1:]
    return stemmer.stem(word)


def split_text(txt):
    """
    Splits text, filters and stems words
    """
    splitted_words = list(
        map(lambda x: word_stem(x),
            filter(lambda x: is_word_useful(x), re.split(r"[\s\n\t]+", txt))
            )
    )
    return splitted_words


def get_all_words(reviews):
    """
    gets list all possible words in reviews
    """
    s = set()
    for review in reviews:
        for w in split_text(review["title"]):
            s.add(w)
    l = list(s)
    return l


def get_map(L):
    return {e: i for i, e in enumerate(L)}


def pull_sim(pull1, pull2):
    """
    counts file path-based similarity for pull1 and pull2
    """
    changed_files1 = pull1["file_path"]
    changed_files2 = pull2["file_path"]
    if len(changed_files1) == 0 or len(changed_files2) == 0:
        return 0
    sum_score = 0
    for f1 in changed_files1:
        s1 = set(f1.split('/'))
        for f2 in changed_files2:
            s2 = set(f2.split('/'))
            sum_score += (len(s1 & s2)) / max(len(s1), len(s2))
    ret = sum_score / (len(changed_files1) * len(changed_files2) + 1)
    return ret
