import json
import re
import numpy as np
from tqdm import tqdm
from nltk.corpus import stopwords
import nltk
import pprint

nltk.download('stopwords')
words = set(nltk.corpus.words.words())


def remove_nonsense(review):
    return " ".join(w for w in nltk.wordpunct_tokenize(review) \
                    if w.lower() in words or not w.isalpha())


def calculate_relevance_score(unique_words, reviews):
    reviews_safety_hazard = [review["Review"] for review in reviews if review['Safety hazard'] == 1]
    reviews_not_safety_hazard = [review["Review"] for review in reviews if review['Safety hazard'] == 0]

    word_relevance_score = {}

    for word in tqdm(unique_words):
        if len(word) == 1:
            continue
        A = sum(word in review.split() for review in reviews_safety_hazard)
        C = len(reviews_safety_hazard) - A

        B = sum(word in review.split() for review in reviews_not_safety_hazard)
        D = len(reviews_not_safety_hazard) - B

        if A + B + C + D < 0:
            print ('1:', A + B + C +D)
            print(word)

        if (A + B) * (C + D) < 0:
            print ('2:', (A+B) * (C+D))
            print(word)

        score = (np.sqrt(A + B + C + D) * (A * D - C * B)) / (np.sqrt((A + B) * (C + D)))
        word_relevance_score[word] = score

    word_relevance_score_4k = dict(filter(lambda a: a[1] >= 4000, word_relevance_score.items()))
    word_relevance_score_4k = dict(reversed(sorted(word_relevance_score_4k.items(), key=lambda item: item[1])))
    pprint.pprint(word_relevance_score_4k)
    return word_relevance_score_4k


def preprocess_data(reviews: list):
    """
    Process reviews and return list of unique words
    :param reviews:
    :return: unique words
    """

    for review in reviews:
                ## Lower all review
        review["Review"] = review["Review"].lower()

        ## Remove special character from string
        regex1 = r"[^\w+\d+\']+"
        review["Review"] = re.sub(regex1, ' ', review["Review"]).strip()

    ## Get unique word list
    review_list = [review["Review"].split(" ") for review in reviews]
    unique_words = set().union(*review_list)

    ## Remove stop words
    stop_words = set(stopwords.words('english'))
    unique_words = unique_words.difference(stop_words)

    return unique_words, reviews


def main():
    ## Get reviews data from url
    with open('applicance_reviews.json', 'r') as file:
        request_reviews = file.read()

    try:
        reviews = json.loads(request_reviews)

        ## Pre-process data
        unique_words, reviews = preprocess_data(reviews)

        ## Calculate relevance score
        relevance_scrore = calculate_relevance_score(unique_words, reviews)
        count = 0
        for word in relevance_scrore:
            if relevance_scrore[word] > 4000:
                print(word)
                count += 1
        print(count)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
