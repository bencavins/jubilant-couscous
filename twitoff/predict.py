import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import vectorize_tweet


def predict_user(username0, username1, hypo_tweet_text):
    """
    Determine which user is more likely to say hypothetical tweet.
    """
    # Grab both users from db
    user0 = User.query.filter(User.username == username0).one()
    user1 = User.query.filter(User.username == username1).one()

    # Grab tweet vectors from each users's tweets
    user0_vectors = np.array([tweet.vector for tweet in user0.tweets])
    user1_vectors = np.array([tweet.vector for tweet in user1.tweets])

    # Stack tweet vectors to get one np array
    vectors = np.vstack([user0_vectors, user1_vectors])
    labels = np.concatenate(
        [np.zeros(len(user0.tweets)), np.ones(len(user1.tweets))]
    )

    # fit the model with our x's == vectors & our y's == labels
    log_reg = LogisticRegression().fit(vectors, labels)

    # vectorize the hypothetical tweet text
    hypo_tweet_vector = vectorize_tweet(hypo_tweet_text)

    return log_reg.predict(hypo_tweet_vector.reshape(1, -1))