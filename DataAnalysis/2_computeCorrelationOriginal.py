import numpy as np
import pandas as pd
import scipy.stats as stats
from style import styles, style_max
import dataframe_image as dfi

# Import test results
test_scores_constant = pd.read_csv("./DataAnalysis/test_data/scores_C.csv")
test_scores_human = pd.read_csv("./DataAnalysis/test_data/scores_H.csv")


# Import metric scores
Toussaint_human = pd.read_csv('./DataAnalysis/metric_scores/Toussaint_H.csv') 
Toussaint_constant = pd.read_csv('./DataAnalysis/metric_scores/Toussaint_C.csv')

LHL_human = pd.read_csv('./DataAnalysis/metric_scores/LHL_H.csv') 
LHL_constant = pd.read_csv('./DataAnalysis/metric_scores/LHL_C.csv')

Pressing_human = pd.read_csv('./DataAnalysis/metric_scores/Pressing_H.csv') 
Pressing_constant = pd.read_csv('./DataAnalysis/metric_scores/Pressing_C.csv')

WNBD_human = pd.read_csv('./DataAnalysis/metric_scores/WNBD_H.csv') 
WNBD_constant = pd.read_csv('./DataAnalysis/metric_scores/WNBD_C.csv')

OffBeatness_human = pd.read_csv('./DataAnalysis/metric_scores/OffBeatness_H.csv') 
OffBeatness_constant = pd.read_csv('./DataAnalysis/metric_scores/OffBeatness_C.csv')

IOI_human = pd.read_csv('./DataAnalysis/metric_scores/IOI_informationEntropy_H.csv') 
IOI_constant = pd.read_csv('./DataAnalysis/metric_scores/IOI_informationEntropy_C.csv')


# Compute mean scores 
mean_test_scores_H = test_scores_human.mean(axis=0)
mean_test_scores_C = test_scores_constant.mean(axis=0)

# Rename index (only keep velocity mode and rhythm number)
for i in mean_test_scores_H.index:
    mean_test_scores_H = mean_test_scores_H.rename(index={i : i.split('_')[1]})
for i in mean_test_scores_C.index:
    mean_test_scores_C = mean_test_scores_C.rename(index={i : i.split('_')[1]})

# Init lists of correlation coefficients
pearson_originalMetrics_C_list = []
pearson_originalMetrics_H_list = []
spearman_originalMetrics_C_list = []
spearman_originalMetrics_H_list = []

metric_pearson_list = []
metric_spearman_list = []

# For all metric obtain correlation table
for metric_constant, metric_human, name in [[Toussaint_constant, Toussaint_human, 'Toussaint'], 
                                            [LHL_constant,LHL_human, 'LHL'], 
                                            [Pressing_constant, Pressing_human, 'Pressing'],
                                            [WNBD_constant, WNBD_human, 'WNBD'], 
                                            [IOI_constant, IOI_human, 'IOIinformationEntropy'],
                                            [OffBeatness_constant, OffBeatness_human, 'OffBeatness']]:
    
    # Take the rhythm for the index
    metric_constant = metric_constant.set_index('Rhythm')
    metric_human = metric_human.set_index('Rhythm')

    # Only keep order number and velocity mode letter
    for i in metric_constant.index:
        metric_constant = metric_constant.rename(index={i: i.split('_')[0]+'C'})
    for i in metric_human.index:
        metric_human = metric_human.rename(index={i: i.split('_')[0]+'H'})

    # Get pd series for correlation and sort values 
    original_metric_scores_C = metric_constant['Original '+name].sort_values()
    original_metric_scores_H = metric_human['Original '+name].sort_values()

    # Sort test scores according to metric ones
    sorted_mean_test_C_original = mean_test_scores_C.reindex(original_metric_scores_C.index)
    sorted_mean_test_H_original = mean_test_scores_H.reindex(original_metric_scores_H.index)

    # Compute Pearson coefficients
    Pearson_originalMetric_C = stats.pearsonr(original_metric_scores_C.values, sorted_mean_test_C_original.values)[0]
    Pearson_originalMetric_H = stats.pearsonr(original_metric_scores_H.values, sorted_mean_test_H_original.values)[0]

    # Compute Spearman coefficients
    Spearman_originalMetric_C = stats.spearmanr(original_metric_scores_C.values, sorted_mean_test_C_original.values)[0]
    Spearman_originalMetric_H = stats.spearmanr(original_metric_scores_H.values, sorted_mean_test_H_original.values)[0]

    # Append coefficients in lists for table
    pearson_originalMetrics_C_list.append(Pearson_originalMetric_C)
    pearson_originalMetrics_H_list.append(Pearson_originalMetric_H)
    spearman_originalMetrics_C_list.append(Spearman_originalMetric_C)
    spearman_originalMetrics_H_list.append(Spearman_originalMetric_H)

print(pearson_originalMetrics_H_list)

# Create lists for rows of pearson and spearman df
metric_pearson_list = [pearson_originalMetrics_C_list, pearson_originalMetrics_H_list]
metric_spearman_list = [spearman_originalMetrics_C_list, spearman_originalMetrics_H_list]

print(metric_pearson_list)

# Create df for pearson correlations
pearson_original = pd.DataFrame(metric_pearson_list)
pearson_original.rename(index={0:'Constant',1:'Performed'}, inplace=True) 
pearson_original.rename(columns={0:'Toussaint', 1:'LHL', 2:'Pressing', 3:'WNBD', 4:'IOI Entropy',5: 'Off-Beatness'}, inplace=True)

# Create df for spearman correlations
spearman_original = pd.DataFrame(metric_spearman_list)
spearman_original.rename(index={0:'Constant',1:'Human'}, inplace=True) 
spearman_original.rename(columns={0:'Toussaint', 1:'LHL', 2:'Pressing', 3:'WNBD', 4:'IOIEntropy',5: 'OffBeatness'}, inplace=True)



print(spearman_original)


# Style tables   
pearson_styled = pearson_original.style.set_caption('Pearson Coefficient Comparison')
pearson_styled.set_table_styles(styles)

spearman_styled = spearman_original.style.set_caption('Spearman Coefficient Comparison')
spearman_styled.set_table_styles(styles)

# Underline max 
# max_index_pearson = pearson_original.values.argmax()
# max_row_pearson, max_col_pearson = divmod(max_index_pearson, pearson_original.shape[1])
# pearson_styled.apply(style_max, max_row=max_row_pearson, max_col=max_col_pearson, axis=None)

max_index_spearman = spearman_original.values.argmax()
max_row_spearman, max_col_spearman = divmod(max_index_spearman, spearman_original.shape[1])
spearman_styled.apply(style_max, max_row=max_row_spearman, max_col=max_col_spearman, axis=None)

# Save tables
dfi.export(pearson_styled, f'./DataAnalysis/correlation_tables/OriginalMetrics_Pearson.png')
dfi.export(spearman_styled, f'./DataAnalysis/correlation_tables/OriginalMetrics_Spearman.png')
