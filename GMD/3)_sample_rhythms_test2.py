import pretty_midi
import numpy as np
import os
import pandas as pd
import shutil
import math
import random 




#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-. SAMPLE RHYTHMS TEST2 -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-#

# Run this script to select only 10 polyphonic rhythmic patterns among the reduced bars obtained from GMD
# (the selection is based on the expected complexity score computed with Polyphonic Toussaint and on the velocity variance)

#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-#



# Import df with all rhythms scored by original and velocity Toussaint
rhythms_scores = pd.read_csv("./GMD/all_rhythms_score_reduced.csv")


# Only keep velocity Toussaint score
rhythms_scores = rhythms_scores.iloc[::,[0,1,3]]


# Sort according to score
sorted_rhythms_scores = rhythms_scores.sort_values(by=['Original Score']).reset_index(drop=True)

# SAMPLE n rhythms equally spaced
n = 10                                          # change here to select how many rhythms to choose

groups = np.array_split(sorted_rhythms_scores, n)                   # divided in 10 groups
all_rhythms_directory = './GMD/GMD_reduced_bars/'
sampled_rhythms_directory2 = './GMD/sampled/human_velocity/'

for i in range(len(groups)):                        #find rhythm with max var in each group
    group = groups[i] 
    group = group.reset_index(drop=True)
    if i==0: group = group.loc[:10]
    last_idx = group.index[-1]

    proposals = (group.sort_values(by=['Var2'], ascending=False)).reset_index(drop=True).head(100)
    idx = random.randint(proposals.index[0], proposals.index[-1])
    rhythm = group.loc[idx]

    name = rhythm['Rhythm']
   
    rhythm_path_src = all_rhythms_directory + name + '.mid'
    rhythm_path_dst =  sampled_rhythms_directory2 + str(i) + '_' + name + '.mid' 
    shutil.copy(rhythm_path_src, rhythm_path_dst)




# #  Copy the selected rhytms in apposite folder (here approach 2 is chosen)

all_rhythms_directory = './GMD/GMD_reduced_bars/'
sampled_rhythms_directory = './GMD/sampled/human_velocity/'

# # Get sampled rhythms version with constant velocity
data = pd.DataFrame({'Rhythm': [], 'Original Score': [], 'Var2': []})
for file in os.listdir(sampled_rhythms_directory):
    path = os.path.join(sampled_rhythms_directory, file)
    if path[-3:] == 'mid':

        # Build df with score
        name= file[2:-4]
        print(name)
        idx = (sorted_rhythms_scores.index[sorted_rhythms_scores['Rhythm']==name].tolist())
        print(file[:2], sorted_rhythms_scores.loc[idx])
        
print(data)


# Get sampled rhythms version with constant velocity
for file in os.listdir(sampled_rhythms_directory):
    path = os.path.join(sampled_rhythms_directory, file)
    if path[-3:] == 'mid':
        name_ext = os.path.basename(path)
        name = os.path.splitext(name_ext)[0]
        pm = pretty_midi.PrettyMIDI(path)
        for note in pm.instruments[0].notes:
            note.velocity = 100
        pm.write(f'./GMD/sampled/constant_velocity/{name}_constant.mid')




