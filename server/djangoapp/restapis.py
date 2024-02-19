import requests
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

# Create a `get_request` to make HTTP GET requests
def get_request(url, **kwargs):
    response = None
    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
        response.raise_for_status()  # Raise exception for non-200 status codes
    except requests.exceptions.RequestException as e:
        print(f"Network exception occurred: {e}")
    return response.json() if response else None


# Create a `post_request` to make HTTP POST requests
def post_request(url, json_payload, **kwargs):
    try:
        response = requests.post(url, json=json_payload, params=kwargs)
        response.raise_for_status()  # Raise exception for non-200 status codes
    except requests.exceptions.RequestException as e:
        print(f"Network exception occurred: {e}")
    return response.json() if response else None


# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url, **kwargs)
    if json_result:
        for dealer in json_result:
            dealer_obj = CarDealer(
                address=dealer.get("address", ""),
                city=dealer.get("city", ""),
                full_name=dealer.get("full_name", ""),
                id=dealer.get("id", None),
                lat=dealer.get("lat", None),
                long=dealer.get("long", None),
                short_name=dealer.get("short_name", ""),
                st=dealer.get("st", ""),
                zip=dealer.get("zip", "")
            )
            results.append(dealer_obj)
    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url, **kwargs)
    if json_result:
        for dealer_review in json_result:
            sentiment = analyze_review_sentiments(dealer_review['review'])
            reviews_obj = DealerReview(
                dealership=dealer_review.get("dealership", None),
                name=dealer_review.get("name", ""),
                purchase=dealer_review.get("purchase", False),
                id=dealer_review.get("id", None),
                review=dealer_review.get("review", ""),
                purchase_date=dealer_review.get("purchase_date", None),
                car_make=dealer_review.get("car_make", ""),
                car_model=dealer_review.get("car_model", ""),
                car_year=dealer_review.get("car_year", None),
                sentiment=sentiment
            )
            results.append(reviews_obj)
    return results
    

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(dealer_review):
    url = "https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/12e28df9-561f-4f7c-a990-930cafab8693"
    api_key = "JlzUd-wpuuGngIx0RqgyDhnbmnsAktRjStec3BaHYzi0"

    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url(url)

    try:
        response = natural_language_understanding.analyze(
            text=dealer_review,
            features=Features(sentiment=SentimentOptions())
        ).get_result()
        return response['sentiment']['document']['score']
    except Exception as e:
        print(f"Exception occurred during sentiment analysis: {e}")
        return 0