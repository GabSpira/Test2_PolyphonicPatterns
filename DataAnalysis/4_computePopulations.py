import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import re



# Import test results (10 columns (rhythms), 80 rows (users))
test_scores_constant = pd.read_csv("./DataAnalysis/test_data/scores_C.csv")
test_scores_human = pd.read_csv("./DataAnalysis/test_data/scores_H.csv")

print(test_scores_constant)
# All scores: rename index (only keep velocity mode and rhythm number)
for i in test_scores_constant.columns:
    test_scores_constant = test_scores_constant.rename(columns={i : i.split('_')[1][0]})
for i in test_scores_human.columns:
    test_scores_human = test_scores_human.rename(columns={i : i.split('_')[1][0]})


# Mean score for each user               (80 length array, averaged column-wise)
user_mean_scores_C = test_scores_constant.mean(axis=1)
user_mean_scores_H = test_scores_human.mean(axis=1)

# Mean score for each pattern               (10 length array, averaged row-wise)
pattern_mean_scores_C = test_scores_constant.mean(axis=0)
pattern_mean_scores_H = test_scores_human.mean(axis=0)


# Mean complexity shift for user 
mean_shift_user = round(user_mean_scores_H - user_mean_scores_C, 1)

# Mean complexity shift for pattern
mean_shift_pattern = round(pattern_mean_scores_H - pattern_mean_scores_C,1)

print(mean_shift_pattern)

values, counts = np.unique(mean_shift_user, return_counts=True)


# Background of the plot
sns.set(style="whitegrid")

# Plot 4 histograms next to each other
plt.figure(figsize=(10, 4))
plt.bar(values, counts, color='#f74c7e', edgecolor='#f74c7e', width=0.07, alpha=0.7)

# Plot settings
title = 'Users Mean Perceived Complexity Shifts (Human vs Constant) Distribution - Raw Data'
path = './DataAnalysis/populations/distribution of shifts perceived by each user.png'
plt.suptitle(title, fontsize=16, fontweight='bold', y=0.96, x=0.5, bbox=dict(boxstyle='square, pad=0.5', ec=(1., 0.5, 0.5), facecolor='#FFF7DA'))
plt.xlabel('Mean Displacement for User', fontsize = 16)
plt.ylabel('Frequency', fontsize =16)
plt.axvline(x=0, color='red', linestyle='dotted')
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.tight_layout()
# plt.show()
plt.savefig(path)    






##  INSPECT HOW THE USERS PATTERN SCORES ARE DISTRIBUTED IN EACH VELOCITY MODE WITH RESPECT TO PATTERN MEAN SCORE

# Mean complexity of each pattern
pattern_mean_score_C = test_scores_constant.mean(axis=0)
pattern_mean_score_H = test_scores_human.mean(axis=0)

# Find Constant mode shifts in each pattern with respect to mean score
difference_from_mean_C_df = pd.DataFrame(index=test_scores_constant.index ,columns=test_scores_constant.columns)
for user in test_scores_constant.index:
    difference_from_mean_C = round(pattern_mean_score_C - test_scores_constant.loc[user],1)
    for rhythm in difference_from_mean_C.index:
        difference_from_mean_C_df.loc[user, [rhythm]] = [difference_from_mean_C[rhythm]]

# Get values for plot
flatten_difference_C = difference_from_mean_C_df.values.flatten()
values_difference_C, counts_difference_C = np.unique(flatten_difference_C, return_counts=True)

# Find Human mode shifts in each pattern with respect to mean score
difference_from_mean_H_df = pd.DataFrame(index=test_scores_human.index ,columns=test_scores_human.columns)
for user in test_scores_human.index:
    difference_from_mean_H = round(pattern_mean_score_H - test_scores_human.loc[user],1)
    for rhythm in difference_from_mean_H.index:
        difference_from_mean_H_df.loc[user, [rhythm]] = [difference_from_mean_H[rhythm]]

# Get values for plot
flatten_difference_H = difference_from_mean_H_df.values.flatten()
values_difference_H, counts_difference_H = np.unique(flatten_difference_H, return_counts=True)




# Plot 2 histograms next to each other
plt.gca()
sns.set(style="whitegrid")
fig, axes = plt.subplots(2, 1, figsize=(10, 6),  gridspec_kw={'hspace': 0.35}, sharex='col')

sns.histplot(flatten_difference_C, ax=axes[0], color='#83a5de', stat='density')
# sns.kdeplot(difference_from_mean_C, color='#83a5de', ax=axes[0], alpha=1, bw=0.2)
axes[0].axvline(x=0, color='red', linestyle='dotted')
axes[0].set_title('Constant Mode: User\'s Rhythm Score shift with respect to Mean Rhythm Score', fontdict={'fontsize': 10, 'fontweight': 'bold'})
box = axes[0].get_position()
box.y0 = box.y0 - 0.065 
box.y1 = box.y1 - 0.065
axes[0].set_position(box)

# axes[1].bar(values_difference_H, counts_difference_H, color='#f74c7e', edgecolor='#f74c7e', width=0.07, alpha=0.7)
sns.histplot(flatten_difference_H, ax=axes[1], color='#f74c7e', stat='density')
# sns.kdeplot(-difference_from_mean_H, color='#f74c7e', ax=axes[1], alpha=1, bw=0.6)

axes[1].axvline(x=0, color='red', linestyle='dotted')
axes[1].set_title('Human Mode: User\'s Rhythm Score shift with respect to Mean Rhythm Score', fontdict={'fontsize': 10, 'fontweight': 'bold'})
box = axes[1].get_position()
box.y0 = box.y0 - 0.02
box.y1 = box.y1 - 0.02
axes[1].set_position(box)

# Plot settings
title = 'Comparison between Distributions \nUser\'s scores difference with respect to Pattern\'s mean scores in each Velocity Mode - Raw Data'
path = './DataAnalysis/populations/Distribution Comparison - Users scores displacements from mean score of each pattern - Raw Data (2).png'
plt.suptitle(title, fontsize=13, fontweight='bold', y=0.96, x=0.5, bbox=dict(boxstyle='square, pad=0.5', ec=(1., 0.5, 0.5), facecolor='#FFF7DA'))
plt.xlabel('')
plt.tight_layout()
# plt.show()
plt.savefig(path) 

