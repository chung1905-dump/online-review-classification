import requests
import json
import re
import numpy as np
from tqdm import tqdm
from nltk.corpus import stopwords
import nltk
import pprint

nltk.download('stopwords')
nltk.download('words')
words = set(nltk.corpus.words.words())


def remove_nonsense(review):
    return " ".join(w for w in nltk.wordpunct_tokenize(review) \
                    if w.lower() in words or not w.isalpha())


def calculate_relevance_score(unique_words, reviews):
    reviews_safety_hazard = [review["Review"] for review in reviews if review['Safety hazard'] == 1]
    reviews_not_safety_hazard = [review["Review"] for review in reviews if review['Safety hazard'] == 0]

    word_relevance_score = {}

    for word in tqdm(unique_words):
        A = sum(word in review.split() for review in reviews_safety_hazard)
        C = len(reviews_safety_hazard) - A

        B = sum(word in review.split() for review in reviews_not_safety_hazard)
        D = len(reviews_safety_hazard) - B

        score = (np.sqrt(A + B + C + D) * (A * D - C * B)) / (np.sqrt((A + B) * (C + D)))
        word_relevance_score[word] = score
    word_relevance_score = dict(filter(lambda a: a[1] >= 4000, word_relevance_score.items()))
    word_relevance_score = dict(reversed(sorted(word_relevance_score.items(), key=lambda item: item[1])))
    pprint.pprint(word_relevance_score)
    return word_relevance_score


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

        ## Remove nonsense words
        # review["Review"] = remove_nonsense(review["Review"])

    ## Get unique word list
    review_list = [review["Review"].split(" ") for review in reviews]
    unique_words = set().union(*review_list)

    ## Remove stop words
    # stop_words = set(stopwords.words('english'))
    # unique_words = unique_words.difference(stop_words)
    # unique_words = [x for x in unique_words if len(x) > 2]

    return unique_words, reviews


def main():
    ## Get reviews data from url
    request_reviews = requests.get(url="https://dgoldberg.sdsu.edu/515/appliance_reviews.json")
    try:
        reviews = json.loads(request_reviews.text)

        ## Pre-process data
        unique_words, reviews = preprocess_data(reviews)

        ## Calculate relevance score
        relevance_scrore = calculate_relevance_score(unique_words, reviews)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
