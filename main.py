import requests
import json
import re


def calculate_relevance_score():
    pass


def preprocess_data(reviews: list):
    """
    Process reviews and return list of unique words
    :param reviews:
    :return: unique words
    """
    ## Lower all review
    reviews_lower = [review["Review"].lower() for review in reviews]

    ## Remove special character from string
    regex = r"[^\w+\d+\']+"
    reviews_lower = [re.sub(regex, ' ', review).strip() for review in reviews_lower]
    reviews_lower = [review.split(" ") for review in reviews_lower]

    ## Get unique word list
    unique_words = set().union(*reviews_lower)
    return unique_words


def main():
    ## Get reviews data from url
    request_reviews = requests.get(url="https://dgoldberg.sdsu.edu/515/appliance_reviews.json")
    try:
        reviews = json.loads(request_reviews.text)

        ## Pre-process data
        request_reviews = preprocess_data(reviews)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
