import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from numpy import random
import random
import matplotlib as mpl
import matplotlib.lines as mlines

# Seed
random.seed(0)

def linear_regression_model(x, y, std, metric, vel_mode, algorithm):

    x = x.reshape(-1,1)
    y = y.reshape(-1,1)

    # Fit model
    model = LinearRegression()
    model.fit(x, y)

    # Predict and compute mean error 
    predictions = model.predict(x)
    e = mean_absolute_error(y, predictions)

    # Plot 
    plt.figure(figsize=(10, 6))

    # Standard Deviations of mean subjective ratings
    for i in range(len((std))):
        plt.plot([x[i], x[i]], [y[i] - std[i]/2, y[i] + std[i]/2], color='#377CE4', linewidth=2, alpha=0.85)
    plt.plot(0,0,  color='#377CE4', label = 'Standard Deviation')

    # Plot linear regression line and subjective ratings
    plt.scatter(x, y, label='Mean Subjective Ratings', color = '#377CE4')
    plt.plot(x, predictions, color='#FF741E', linestyle='dashed', alpha=0.9, label='Linear Regression')

    # Plot settings
    plt.yticks(fontsize=14)
    plt.xticks(fontsize=14)
    plt.xlabel(f'{metric} Metric Scores', fontsize=16) 
    plt.ylabel('Subjective Ratings', fontsize=16) 
    plt.grid(True)
    plt.legend(loc='upper left', fontsize = 15)
    title = 'Linear Regression Model, ' + metric + ' Metric, Velocity Mode: ' + vel_mode
    plt.suptitle(title, fontsize=10, fontweight='bold', y=0.96, x=0.5, bbox=dict(boxstyle='square, pad=0.5', ec=(1., 0.5, 0.5), facecolor='#FFF7DA'))

    # Coefficient of Determination
    R2 = model.score(x, y)

    # Compute line parameters
    q = model.intercept_[0]
    m = model.coef_[0][0]
    print(f'You can get a coefficient of determination R^2 = {round(R2,4)} with the linear model: y = {round(m,4)}*x + {round(q,4)}')

    # Add equation and R^2 text box
    equation = f'y = {round(m, 4)}*x + {round(q, 4)}'
    r_squared = f'R^2 = {round(R2, 4)}'
    text_box = f'Equation: {equation}\n{r_squared}'
    plt.text(0.95, 0.05, text_box, transform=plt.gca().transAxes, fontsize=16,
            verticalalignment='bottom', horizontalalignment='right', bbox=dict(boxstyle='round', facecolor='#edf4ff', alpha=1))

    # Save graph
    path = f'./DataAnalysis/linear_regression_models/Linear_{algorithm}_{metric}_{vel_mode}.png'
    plt.savefig(path)
    # plt.show()




def linear_regression_model2(x, y, std, metric, vel_mode, algorithm):

    x = x.reshape(-1,1)
    y = y.reshape(-1,1)

    # Fit model
    model = LinearRegression()
    model.fit(x, y)

    # Predict and compute mean error 
    predictions = model.predict(x)
    e = mean_absolute_error(y, predictions)

    # Plot 
    plt.figure(figsize=(9, 8))

    # Standard Deviations of mean subjective ratings
    for i in range(len((std))):
        plt.plot([x[i], x[i]], [y[i] - std[i]/2, y[i] + std[i]/2], color='#377CE4', linewidth=2, alpha=0.85)
    plt.plot(0,0,  color='#377CE4', label = 'Standard Deviation')

    # Plot linear regression line and subjective ratings
    plt.scatter(x, y, label='Mean Subjective Ratings', color = '#377CE4')
    plt.plot(x, predictions, color='#FF741E', linestyle='dashed', alpha=0.9, label='Linear Regression')

    # Plot settings
    plt.yticks(fontsize=18)
    plt.xticks(fontsize=18)
    plt.xlabel(f'{metric} Metric Scores', fontsize=20) 
    plt.ylabel('Subjective Ratings', fontsize=20) 
    plt.grid(True)
    plt.legend(loc='lower right', fontsize = 22)
    title = 'Linear Regression Model, ' + metric + ' Metric, Velocity Mode: ' + vel_mode
    # plt.suptitle(title, fontsize=10, fontweight='bold', y=0.96, x=0.5, bbox=dict(boxstyle='square, pad=0.5', ec=(1., 0.5, 0.5), facecolor='#FFF7DA'))

    # Coefficient of Determination
    R2 = model.score(x, y)

    # Compute line parameters
    q = model.intercept_[0]
    m = model.coef_[0][0]
    print(f'You can get a coefficient of determination R^2 = {round(R2,4)} with the linear model: y = {round(m,4)}*x + {round(q,4)}')

    # Add equation and R^2 text box
    equation = f'y = {round(m, 4)}*x + {round(q, 4)}'
    r_squared = f'R^2 = {round(R2, 4)}'
    text_box = f'Equation: {equation}\n{r_squared}'
    plt.text(0.05, 0.95, text_box, transform=plt.gca().transAxes, fontsize=20,
            verticalalignment='top', horizontalalignment='left', bbox=dict(boxstyle='round', facecolor='#edf4ff', alpha=1))

    # Save graph
    path = f'./DataAnalysis/linear_regression_models/Linear_{algorithm}_{metric}_{vel_mode}.png'
    plt.tight_layout()
    plt.savefig(path)
    # plt.show()




def violin(x, y, std, scores, metric, vel_mode):

    # Plot 
    plt.figure(figsize=(16, 8))

    # print(scores.columns)
    sns.violinplot(data=scores, width=1)
    # plt.violinplot(scores)

    #  # Standard Deviations of mean subjective ratings
    # for i in range(len((std))):
    #     plt.plot([x[i], x[i]], [y[i] - std[i]/2, y[i] + std[i]/2], color='#377CE4', linewidth=2, alpha=0.85)
    #     sns.violinplot(scores.iloc[i])
    # plt.plot(0,0,  color='#377CE4', label = 'Standard Deviation')


    # Plot settings
    plt.yticks(fontsize=20)
    plt.xticks(fontsize=20)
    plt.xlabel(f'Rhythms', fontsize=22) 
    plt.ylabel('Subjective Ratings', fontsize=22) 
    plt.grid(True)
    # plt.legend(loc='upper left', fontsize = 15)
    title = 'Linear Regression Model, ' + metric + ' Metric, Velocity Mode: ' + vel_mode
    # plt.suptitle(title, fontsize=10, fontweight='bold', y=0.96, x=0.5, bbox=dict(boxstyle='square, pad=0.5', ec=(1., 0.5, 0.5), facecolor='#FFF7DA'))

    params = {'axes.labelsize': 28, 'xtick.labelsize': 18, 'ytick.labelsize': 18}
    mpl.rcParams.update(params)

    # Save graph
    path = f'./DataAnalysis/violin/Violin_{vel_mode}.png'
    plt.savefig(path)
    # plt.show()



def tot_Scatter(x, y_tot, metric, vel_mode, algorithm):

    x = x.reshape(-1,1)
    
    mean = y_tot.mean()

    # Fit model
    model = LinearRegression()
    model.fit(x, mean)

    # Predict and compute mean error 
    predictions = model.predict(x)

    # Plot 
    plt.figure(figsize=(10, 6))

    # Color settings
    cmap = mpl.cm.Blues(np.linspace(0,1,20))
    cmap = mpl.colors.ListedColormap(cmap[10:,:-1])

    # Plot Scatter of all subjective ratings
    for index, row in y_tot.iterrows():
        offset = index/80 * random.choice([-1, 1])
        distance_from_mean = np.sqrt(100/abs(mean - row))*1.5
        plt.scatter(x, row+offset, s=distance_from_mean, cmap=cmap, alpha=0.35, c=distance_from_mean)
    
    color_bar = plt.colorbar(label='Distance from mean value')
    color_bar.set_alpha(0.7)
    color_bar.draw_all()

    dot = mlines.Line2D([], [], color='#477fb6', marker='o', linestyle='None',
                            markersize=4, label='Subjective Ratings wrt Metric Scores')
     
    line, = plt.plot(x, predictions, color='#FF741E', linestyle='dashed', alpha=0.9, label='Linear Regression')

    plt.legend(handles=[dot, line], loc='upper left')

    # Plot settings
    plt.xlabel(f'{metric} Metric Scores') 
    plt.ylabel('Subjective Ratings') 
    plt.grid(True)
    title = 'All subjective ratings with respect to ' + metric + ' Metric, Velocity Mode: ' + vel_mode
    plt.suptitle(title, fontsize=8, fontweight='bold', y=0.96, x=0.5, bbox=dict(boxstyle='square, pad=0.5', ec=(1., 0.5, 0.5), facecolor='#FFF7DA'))

    # Save graph
    plt.tight_layout()
    path = f'./DataAnalysis/scatter_all_ratings/Scatter_{algorithm}_{metric}_{vel_mode}.png'
    plt.savefig(path)
    # plt.show()


def linear_regression_model_userSTD(x, y, std, metric, vel_mode, algorithm):

    x = x.reshape(-1,1)
    y = y.reshape(-1,1)

    # Fit model
    model = LinearRegression()
    model.fit(x, y)

    # Predict and compute mean error 
    predictions = model.predict(x)
    e = mean_absolute_error(y, predictions)

    # Plot 
    plt.figure(figsize=(10, 6))

    # Standard Deviations of mean subjective ratings
    for i in range(len((std))):
        plt.plot([x[i], x[i]], [y[i] - std[i]/2, y[i] + std[i]/2], color='#377CE4', linewidth=2, alpha=0.85)
    plt.plot(0,0,  color='#377CE4', label = 'Standard Deviation')

    # Plot linear regression line and subjective ratings
    plt.scatter(x, y, label='Mean Subjective Ratings', color = '#377CE4')
    plt.plot(x, predictions, color='#FF741E', linestyle='dashed', alpha=0.9, label='Linear Regression')

    # Plot settings
    plt.xlabel(f'{metric} Metric Scores') 
    plt.ylabel('Subjective Ratings') 
    plt.grid(True)
    
    title = 'Linear Regression Model, ' + metric + ' Metric, Velocity Mode: ' + vel_mode
    plt.suptitle(title, fontsize=13, fontweight='bold', y=0.96, x=0.5, bbox=dict(boxstyle='square, pad=0.5', ec=(1., 0.5, 0.5), facecolor='#FFF7DA'))

    # Coefficient of Determination
    R2 = model.score(x, y)

    # Compute line parameters
    q = model.intercept_[0]
    m = model.coef_[0][0]
    print(f'You can get a coefficient of determination R^2 = {round(R2,4)} with the linear model: y = {round(m,4)}*x + {round(q,4)}')

    # Add equation and R^2 text box
    equation = f'y = {round(m, 4)}*x + {round(q, 4)}'
    r_squared = f'R^2 = {round(R2, 4)}'
    text_box = f'Equation: {equation}\n{r_squared}'
    plt.text(0.95, 0.05, text_box, transform=plt.gca().transAxes, fontsize=12,
            verticalalignment='bottom', horizontalalignment='right', bbox=dict(boxstyle='round', facecolor='#edf4ff', alpha=1))
    plt.legend(loc='upper left')
    # Save graph
    path = f'./DataAnalysis/linear_regression_models/userSTD/Linear_{algorithm}_{metric}_{vel_mode}.png'
    plt.savefig(path)
    # plt.show()


def tot_Scatter_userSTD(x, y_tot, metric, vel_mode, algorithm):

    x = x.reshape(-1,1)
    
    mean = y_tot.mean()

    # Fit model
    model = LinearRegression()
    model.fit(x, mean)

    # Predict and compute mean error 
    predictions = model.predict(x)

    # Plot 
    plt.figure(figsize=(10, 6))

    # Color settings
    cmap = mpl.cm.Blues(np.linspace(0,1,20))
    cmap = mpl.colors.ListedColormap(cmap[10:,:-1])

    # Plot Scatter of all subjective ratings
    for index, row in y_tot.iterrows():
        offset = index/80 * random.choice([-1, 1])
        distance_from_mean = np.sqrt(100/abs(mean - row))*1.5
        plt.scatter(x, row+offset, s=distance_from_mean, cmap=cmap, alpha=0.35, c=distance_from_mean)
    
    color_bar = plt.colorbar(label='Distance from mean value')
    color_bar.set_alpha(0.7)
    color_bar.draw_all()

    dot = mlines.Line2D([], [], color='#477fb6', marker='o', linestyle='None',
                            markersize=4, label='Subjective Ratings wrt Metric Scores')
     
    line, = plt.plot(x, predictions, color='#FF741E', linestyle='dashed', alpha=0.9, label='Linear Regression')

    plt.legend(handles=[dot, line], loc='upper left')

    # Plot settings
    plt.xlabel(f'{metric} Metric Scores') 
    plt.ylabel('Subjective Ratings') 
    plt.grid(True)
    title = 'All subjective ratings with respect to ' + metric + ' Metric, Velocity Mode: ' + vel_mode
    plt.suptitle(title, fontsize=13, fontweight='bold', y=0.96, x=0.5, bbox=dict(boxstyle='square, pad=0.5', ec=(1., 0.5, 0.5), facecolor='#FFF7DA'))

    # Save graph
    path = f'./DataAnalysis/scatter_all_ratings/userSTD/Scatter_{algorithm}_{metric}_{vel_mode}.png'
    plt.savefig(path)
    # plt.show()