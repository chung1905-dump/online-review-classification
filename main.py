import requests
import json
import re
import numpy as np
from tqdm import tqdm


def calculate_relevance_score(unique_words, reviews):
    reviews_safety_hazard = [review for review in reviews if review['Safety hazard'] == 1]
    reviews_not_safety_hazard = [review for review in reviews if review['Safety hazard'] == 0]

    word_relevance_score = {}

    for word in tqdm(unique_words):
        A = sum(word in review["Review"] for review in reviews_safety_hazard)
        C = len(reviews_safety_hazard) - A

        B = sum(word in review["Review"] for review in reviews_not_safety_hazard)
        D = len(reviews_safety_hazard) - B

        score = (np.sqrt(A + B + C + D) * (A * D - C * B)) / (np.sqrt((A + B) * (C + D)))
        word_relevance_score[word] = score
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
        # reviews_lower = [review["Review"].lower() for review in reviews]

        ## Remove special character from string
        regex = r"[^\w+\d+\']+"
        review["Review"] = re.sub(regex, ' ', review["Review"]).strip()

    ## Get unique word list
    review_list = [review["Review"].split(" ") for review in reviews]
    unique_words = set().union(*review_list)

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
        a = 0
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
