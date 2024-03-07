import pandas as pd
from functions import linear_regression_model2, tot_Scatter, violin





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



# All scores: rename index (only keep velocity mode and rhythm number)
for i in test_scores_constant.columns:
    test_scores_constant = test_scores_constant.rename(columns={i : i.split('_')[1]})
for i in test_scores_human.columns:
    test_scores_human = test_scores_human.rename(columns={i : i.split('_')[1]})


# Compute standard deviation of each rhythm score
test_std_C = test_scores_constant.std()
test_std_H = test_scores_human.std()

# Compute mean scores 
mean_test_scores_H = test_scores_human.mean(axis=0)
mean_test_scores_C = test_scores_constant.mean(axis=0)


# For all metric obtain correlation table
for metric_constant, metric_human, name in [[Toussaint_constant, Toussaint_human, 'Toussaint'], 
                                            [LHL_constant,LHL_human, 'LHL'], 
                                            [Pressing_constant, Pressing_human, 'Pressing'],
                                            [WNBD_constant, WNBD_human, 'WNBD'], 
                                            [OffBeatness_constant, OffBeatness_human, 'OffBeatness']]:
    
    # Take the rhythm for the index
    metric_constant = metric_constant.set_index('Rhythm')
    metric_human = metric_human.set_index('Rhythm')

    # Only keep order number and velocity mode letter
    for i in metric_constant.index:
        metric_constant = metric_constant.rename(index={i: i.split('_')[0]+'C'})
    for i in metric_human.index:
        metric_human = metric_human.rename(index={i: i.split('_')[0]+'H'})

    # Get pd series for linear regression and sort values 
    original_metric_scores_C = metric_constant['Original '+name].sort_values()
    velocity_metric_scores_C = metric_constant['Velocity '+name].sort_values()
    original_metric_scores_H = metric_human['Original '+name].sort_values()
    velocity_metric_scores_H = metric_human['Velocity '+name].sort_values()

    # Sort test scores according to metric ones
    sorted_mean_test_C_original = mean_test_scores_C.reindex(original_metric_scores_C.index)
    sorted_mean_test_C_velocity = mean_test_scores_C.reindex(velocity_metric_scores_C.index)
    sorted_mean_test_H_original = mean_test_scores_H.reindex(original_metric_scores_H.index)
    sorted_mean_test_H_velocity = mean_test_scores_H.reindex(velocity_metric_scores_H.index)

    # Sort test scores std according to metric ones
    sorted_test_std_C_original = test_std_C.reindex(original_metric_scores_C.index)
    sorted_test_std_C_velocity = test_std_C.reindex(velocity_metric_scores_C.index)
    sorted_test_std_H_original = test_std_H.reindex(original_metric_scores_H.index)
    sorted_test_std_H_velocity = test_std_H.reindex(velocity_metric_scores_H.index)

    # Get order from metric
    ordered_columns_original_C = original_metric_scores_C.index
    ordered_columns_original_H = original_metric_scores_H.index
    ordered_columns_velocity_C = velocity_metric_scores_C.index
    ordered_columns_velocity_H = velocity_metric_scores_H.index

    # Sort all test scores according to metric ones
    sorted_test_C_original = test_scores_constant[ordered_columns_original_C]
    sorted_test_H_original = test_scores_human[ordered_columns_original_H]
    sorted_test_C_velocity = test_scores_constant[ordered_columns_velocity_C]
    sorted_test_H_velocity = test_scores_human[ordered_columns_velocity_H]
    print(test_scores_constant)
    
    # Plot graphs, 20 of each kind : # in each velocity mode        (2: Human and Constant),
                                     # for each metric              (5: Toussaint, LHL, Pressing, WNBD, OffBeatness),
                                     # in each algorithm version    (2: Original and Velocity)
    
    # Get linear regression models
    linear_regression_model2(original_metric_scores_C.values, sorted_mean_test_C_original.values, sorted_test_std_C_original.values, name, 'Constant', 'Original')
    linear_regression_model2(original_metric_scores_H.values, sorted_mean_test_H_original.values, sorted_test_std_H_original.values, name, 'Human', 'Original')
    # linear_regression_model(velocity_metric_scores_C.values, sorted_mean_test_C_velocity.values, sorted_test_std_C_velocity.values, name, 'Constant', 'Velocity')
    # linear_regression_model(velocity_metric_scores_H.values, sorted_mean_test_H_velocity.values, sorted_test_std_H_velocity.values, name, 'Human', 'Velocity')

    # # Get linear over scatter of all scores
    # tot_Scatter(original_metric_scores_C.values, sorted_test_C_original , name, 'Constant', 'Original')
    # tot_Scatter(original_metric_scores_H.values, sorted_test_H_original , name, 'Human', 'Original')
    # tot_Scatter(velocity_metric_scores_C.values, sorted_test_C_velocity , name, 'Constant', 'Velocity')
    # tot_Scatter(velocity_metric_scores_H.values, sorted_test_H_velocity , name, 'Human', 'Velocity')
    
    # print(type(original_metric_scores_C.values[0]))
    # violin(original_metric_scores_C.values, sorted_mean_test_C_original.values,  sorted_test_std_C_original, test_scores_constant, name, 'Constant')
    # violin(original_metric_scores_H.values, sorted_mean_test_H_original.values,  sorted_test_std_H_original, test_scores_human, name, 'Human')




    


