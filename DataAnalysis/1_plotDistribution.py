import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt


# In this script you get the splitted for velocity mode dfs of the scores and plot them distribution
# you plot both raw data (histogram) and standardized for user (kde)



# Import df with scores and personal info
results_tot = pd.read_csv("./DataAnalysis/test_data/scores_tot.csv")

# Only take scores
scores_tot = results_tot.iloc[:, 6:26]

# Turn strings into numerical scores to use histplot
vote_mapping = {
    'Very low': 1,
    'Low': 2,
    'Medium': 3,
    'High': 4,
    'Very high': 5
}
scores_tot = scores_tot.applymap(lambda x: vote_mapping.get(x, np.nan))


# Split in velocity mode dfs
scores_C = scores_tot.iloc[:, [o.endswith('C') for o in scores_tot.columns]]
scores_H = scores_tot.iloc[:, [o.endswith('H') for o in scores_tot.columns]]

# Save splitted dfs
scores_C.to_csv("./DataAnalysis/test_data/scores_C.csv", index=False)
scores_H.to_csv("./DataAnalysis/test_data/scores_H.csv", index=False)


# Get array
flatten_C = scores_C.values.flatten()
flatten_H = scores_H.values.flatten()

# Get values and counts
values_C, counts_C = np.unique(flatten_C, return_counts=True)
values_H, counts_H = np.unique(flatten_H, return_counts=True)







# #--- PLOT HISTOGRAM FOR RAW SCORES DISTRIBUTION ----#
    

# # Background of the plot
sns.set(style="whitegrid")

# Plot 4 histograms next to each other
plt.figure(figsize=(17, 5))
plt.bar(values_C-0.15, counts_C, color='#83a5de', edgecolor='#83a5de', alpha=0.6, align='center',  width=0.3)
plt.bar(values_H+0.15, counts_H, color='#f74c7e', edgecolor='#f74c7e', alpha=0.6, width=0.3)

# Legend settings
colors = {'Constant':'#83a5de', 'Performed':'#f74c7e'}         
values = list(colors.keys())
handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in values]
plt.legend(handles, values, fontsize=24)

# Plot settings
title = 'Test 2 - Scores Distribution - Raw Data'
path = './DataAnalysis/distributions/Scores Distribution (raw data).png'
x_label = ['Very low', 'Low', 'Medium', 'High', 'Very high']
plt.suptitle(title, fontsize=13, fontweight='bold', y=0.96, x=0.5, bbox=dict(boxstyle='square, pad=0.5', ec=(1., 0.5, 0.5), facecolor='#FFF7DA'))
plt.gca().set_xticks(range(1,6), x_label, fontsize=24)
plt.xlabel('')
plt.yticks(fontsize=22)
plt.ylabel('Frequency', fontsize=24)
plt.tight_layout()
# plt.show()
plt.savefig(path)    




