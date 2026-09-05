import pandas as pd
import heapq
import numpy as np


def find_similar_houses(user_input, db_feature, db_raw, k=3):
    """
    user_input is scaled and limited not price include there,
    db_features are scaled features for just for our calculation
    db_raw is just row data so we finally so out similar outputs

    """

    my_heap = []

    for index, row in enumerate(db_feature):
        # it's retrun index of db_features and row in list like sturcture

        distance = np.linalg.norm(user_input - row)
        # Taking euclidean distance for our calculation 

        neg_dist = -distance
        # Because heap throw smallest value so we are messing with it

        if len(my_heap) < k:
            heapq.heappush(my_heap, (neg_dist, index))

        else:
            if neg_dist > my_heap[0][0]:
                heapq.heapreplace(my_heap, (neg_dist, index))

            """
            we need if block to make sure the give data is bigger so it thorw smaller number,
            like if the input is like [-40, -30, -20] so,
            if -45 > -40 not it's not needed. But if -21 > -40 yes so replace it
            and it's become [-30, -21, -20] cause it take samaller number first
            """

    # Extracting the winner index with list comprehension
    similar_indices = [idx for (neg_dict, idx) in my_heap]
    return db_raw.iloc[similar_indices].to_dict("records")