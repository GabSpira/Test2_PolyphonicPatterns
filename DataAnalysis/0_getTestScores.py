import pandas as pd
import json
import dataframe_image as dfi
from matplotlib import pyplot as plt
import plotly.express as px
import numpy as np
import seaborn as sns


# Run this script to create the dataframe of the test results



def get_subtest_results(data):

    scores_data = []

    for result in data:
        user_id = {'id': result[0]}
        user_data = result[1]['userData']
        user_ratings = result[1]['userRatings']

        result_data = user_id.copy()
        result_data.update(user_data)

        for rating in user_ratings:
            rhythm = rating['rhythm']
            score = rating['score']
            result_data[rhythm] = score
        scores_data.append(result_data)

    df = pd.DataFrame.from_records(scores_data)
    
    return df


# # Load JSON
test = './output/exportedData_test.json'
with open(test, 'r', encoding='utf-8') as file:
    data = json.load(file)

df = get_subtest_results(data)

# Save df
df.to_csv("./DataAnalysis/test_data/scores_tot.csv", index=False)

print(df.shape)