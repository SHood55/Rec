from scikits.crab import datasets
from scikits.crab.models import MatrixPreferenceDataModel
from scikits.crab.metrics import pearson_correlation
from scikits.crab.similarities import UserSimilarity
from scikits.crab.recommenders.knn import UserBasedRecommender
from scikits.crab.recommenders.knn import ItemBasedRecommender
from scikits.crab.similarities.basic_similarities import ItemSimilarity
import json
import pandas as panda
from pandas.io.json import json_normalize
from sklearn.metrics.pairwise import euclidean_distances
from scikits.crab.recommenders.knn.item_strategies import ItemsNeighborhoodStrategy



global data

def recommend():

    movies = datasets.load_sample_movies()
    #Build the model
    model = MatrixPreferenceDataModel(movies.data)
    #Build the similarity
    similarity = UserSimilarity(model, pearson_correlation)
    #Build the User based recommender
    recommender = UserBasedRecommender(model, similarity, with_preference=True)
    #Recommend items for the user 5 (Toby)
    recommender.recommend(5)

    items_strategy = ItemsNeighborhoodStrategy()
    similarity = ItemSimilarity(model, euclidean_distances)
    recsys = ItemBasedRecommender(model, similarity, items_strategy)
#     recsys.recommend('Leopoldo Pires')

#     >>> recsys.recommend('Leopoldo Pires')
#     ['Just My Luck', 'You, Me and Dupree']
#     >>> #Return the 2 explanations for the given recommendation.
#     >>> recsys.recommended_because('Leopoldo Pires', 'Just My Luck',2)
#     ['The Night Listener', 'Superman Returns']

    try:
        with open('data/data.json') as file:
            print "opening json"
            list = json.load(file)
    except:
        print "no data available"

    global data
    data = json_normalize(list)
    model = MatrixPreferenceDataModel(data)

# beers = df.beer_name.unique()
#     apps = data.Name.unique()
#     simple_distances = []
#     for app1 in apps:
#         print "starting", app1
#         for app2 in apps:
#             if app1 != app2:
#                 row = [app1, app2] + calculateBasicSimilarity(app1, app2)
#                 simple_distances.append(row)

    print data.head(1)
# ALL_FEATURES = ['RedFlags', 'FuzzyValue']

def getRedFlags(app):
    x = 1

def getFuzzyValue(app):
#     mask = data.Name.isin(str(app))
    value = data.sort('FuzzyValue')

# def get_beer_reviews(beer, common_users):
#     mask = (data.review_profilename.isin(common_users)) & (data.beer_name==beer)
#     reviews = data[mask].sort('review_profilename')
#     reviews = reviews[reviews.review_profilename.duplicated()==False]
#     return reviews
# beer_1_reviews = get_beer_reviews(beer_1, common_reviewers)
# beer_2_reviews = get_beer_reviews(beer_2, common_reviewers)
#
# cols = ['beer_name', 'review_profilename', 'review_overall', 'review_aroma', 'review_palate', 'review_taste']
# beer_2_reviews[cols].head()
#
def calculateBasicSimilarity(app1, app2):
    # find common reviewers
#     beer_1_reviewers = data[data.beer_name==beer1].review_profilename.unique()
#     beer_2_reviewers = data[data.beer_name==beer2].review_profilename.unique()
#     common_reviewers = set(beer_1_reviewers).intersection(beer_2_reviewers)
    app1Value = getFuzzyValue(app1)
    app2Value = getFuzzyValue(app2)
    return euclidean_distances(app1Value, app2Value)

