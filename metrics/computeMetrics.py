import pretty_midi
from Velocity_Complexity_Metric import Velocity_Complexity_Metric_Class
from Original_Complexity_Metric import Original_Complexity_Metric_Class
from ComplexityMetricsFunctions import get_velocities
import numpy as np
import os
import pandas as pd



# -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.- COMPUTE METRICS -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.- #

# Run this script to get the dataframes of the complexity score of the selected patterns according to each of the metrics #

# -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.--.-.-.-.-.-. #




def compute_metric_score(directory):

    ToussaintVelocityScores_list=[]
    ToussaintOriginalScores_list=[]
    LonguetHigginsLeeVelocityScores_list=[]
    LonguetHigginsLeeOriginalScores_list=[]
    PressingVelocityScores_list=[]
    PressingOriginalScores_list=[]
    WNBDVelocityScores_list=[]
    WNBDOriginalScores_list=[]
    OffBeatnessVelocityScores_list=[]
    OffBeatnessOriginalScores_list=[]
    names_list = []

    IOIOriginalScores_list = []
    
    for file in os.listdir(directory):

        # Def midi object
        path = os.path.join(directory, file)
        pm = pretty_midi.PrettyMIDI(path)

        # Get BPM from file name
        name_ext = os.path.basename(path)
        name = os.path.splitext(name_ext)[0]
        BPM = int(name.split('_')[3])

        # Get metric grid information from BPM
        bar_duration = 60/BPM * 4                       #bar (in seconds)
        resolution = 16
        tatum = bar_duration/resolution                 #16th note (in seconds)
        length = int(bar_duration/tatum)                #16 (in cells)

        # Def voice group from MEZZA
        k_groupings = {
            1: [36, 38],                # kick and snare
            2: [42],                    # closed hh
            3: [46],                    # open hh
            4: [42, 46],                # open and closed hh
            5: [45],                    # high floor tom
            6: [48, 50],                # low mid and high tom
            7: [51],                    # ride cymbal
            8: [49],                    # crash cymbal
            9: [49, 51]                 # ride and crash crymbals
        }

        # Def list of PrettyMIDI objects, one for group and init them
        separated_instruments = [pretty_midi.PrettyMIDI() for _ in range(len(k_groupings))]
        for i in range(len(k_groupings)):
            instrument = pretty_midi.Instrument(program=0)
            separated_instruments[i].instruments.append(instrument)

        # Apply voice groups
        if pm.instruments != []:
            for note in pm.instruments[0].notes:
                pitch = note.pitch

                # Find group (or groups) the pitch belongs to
                groups = [k for k, pitches in k_groupings.items() if pitch in pitches]

                # Add note to group
                for k in groups:
                    separated_instruments[k - 1].instruments[0].notes.append(note)


        # Apply metric to each group
        groups_Toussaint_scores_velocity = []
        groups_Toussaint_scores_original = []
        groups_LonguetHigginsLee_scores_velocity = []
        groups_LonguetHigginsLee_scores_original = []
        groups_Pressing_scores_velocity = []
        groups_Pressing_scores_original = []
        groups_WNBD_scores_velocity = []
        groups_WNBD_scores_original = []
        groups_OffBeatness_scores_velocity = []
        groups_OffBeatness_scores_original = []

        groups_IOI_scores_original = []

        for i in range(len(separated_instruments)):

            # Def pretty midi object
            pm_group = separated_instruments[i]

            # Get onsets
            onsets_times_group = pm_group.get_onsets()
            onsets_indeces_group = np.unique((onsets_times_group/tatum).astype(int))            # exclude multiple notes at the same time (due to quantization)
            onsets_times_group = onsets_indeces_group*tatum
            
            # Get velocities
            onsets_velocities_group = get_velocities(onsets_times_group, pm_group)

            # Def metric for group
            metrics_velocity = Velocity_Complexity_Metric_Class(length, onsets_indeces_group, onsets_velocities_group)
            metrics_original = Original_Complexity_Metric_Class(length, onsets_indeces_group)

            # Compute metrics (both original and velocity algorithms)
            group_Toussaint_velocity = metrics_velocity.getToussaintComplexity_Velocity()
            group_Toussaint_original = metrics_original.getToussaintComplexity()
            group_LonguetHigginsLee_velocity = metrics_velocity.getLonguetHigginsLeeComplexity_Velocity()
            group_LonguetHigginsLee_original = metrics_original.getLonguetHigginsLeeComplexity()
            group_Pressing_velocity = metrics_velocity.getPressingComplexity_Velocity()
            group_Pressing_original = metrics_original.getPressingComplexity()
            
            if len(onsets_indeces_group)!=0: 
                group_WNBD_velocity = metrics_velocity.getWeightedNotetoBeatDistance_Velocity()
                group_WNBD_original = metrics_original.getWeightedNotetoBeatDistance()
                group_IOI_original = metrics_original.getInformationEntropyComplexity()[0]
            else: 
                group_WNBD_velocity = 0
                group_WNBD_velocity = 0
                group_IOI_original = 0

            group_OffBeatness_velocity = metrics_velocity.getOffBeatnessComplexity_Velocity()
            group_OffBeatness_original = metrics_original.getOffBeatnessComplexity()
            
            # Def weight according to group 
            # w = 1/(i+1)
            w = 1
            
            # Apply weight to metrics
            weighted_group_Toussaint_velocity = group_Toussaint_velocity*w
            weighted_group_Toussaint_original = group_Toussaint_original*w
            weighted_group_LonguetHigginsLee_velocity = group_LonguetHigginsLee_velocity*w
            weighted_group_LonguetHigginsLee_original = group_LonguetHigginsLee_original*w
            weighted_group_Pressing_velocity = group_Pressing_velocity*w
            weighted_group_Pressing_original = group_Pressing_original*w
            weighted_group_WNBD_velocity = group_WNBD_velocity*w
            weighted_group_WNBD_original = group_WNBD_original*w
            weighted_group_OffBeatness_velocity = group_OffBeatness_velocity*w
            weighted_group_OffBeatness_original = group_OffBeatness_original*w
            weighted_group_IOI_original = group_IOI_original*w

            # Collect group metrics
            groups_Toussaint_scores_velocity.append(weighted_group_Toussaint_velocity)
            groups_Toussaint_scores_original.append(weighted_group_Toussaint_original)
            groups_LonguetHigginsLee_scores_velocity.append(weighted_group_LonguetHigginsLee_velocity)
            groups_LonguetHigginsLee_scores_original.append(weighted_group_LonguetHigginsLee_original)
            groups_Pressing_scores_velocity.append(weighted_group_Pressing_velocity)
            groups_Pressing_scores_original.append(weighted_group_Pressing_original)
            groups_WNBD_scores_velocity.append(weighted_group_WNBD_velocity)
            groups_WNBD_scores_original.append(weighted_group_WNBD_original)
            groups_OffBeatness_scores_velocity.append(weighted_group_OffBeatness_velocity)
            groups_OffBeatness_scores_original.append(weighted_group_OffBeatness_original)
            groups_IOI_scores_original.append(weighted_group_IOI_original)

        # Get metrics score for that pattern
        velocity_Toussaint_score_rhythm = sum(groups_Toussaint_scores_velocity)
        original_Toussaint_score_rhythm = sum(groups_Toussaint_scores_original)
        velocity_LonguetHigginsLee_score_rhythm = sum(groups_LonguetHigginsLee_scores_velocity)
        original_LonguetHigginsLee_score_rhythm = sum(groups_LonguetHigginsLee_scores_original)
        velocity_Pressing_score_rhythm = sum(groups_Pressing_scores_velocity)
        original_Pressing_score_rhythm = sum(groups_Pressing_scores_original)
        velocity_WNBD_score_rhythm = sum(groups_WNBD_scores_velocity)
        original_WNBD_score_rhythm = sum(groups_WNBD_scores_original)
        velocity_OffBeatness_score_rhythm = sum(groups_OffBeatness_scores_velocity)
        original_OffBeatness_score_rhythm = sum(groups_OffBeatness_scores_original)
        original_IOI_score_rhythm = sum(groups_IOI_scores_original)

        # Collect rhythm info in lists to build a df
        ToussaintVelocityScores_list.append(velocity_Toussaint_score_rhythm)
        ToussaintOriginalScores_list.append(original_Toussaint_score_rhythm)
        LonguetHigginsLeeVelocityScores_list.append(velocity_LonguetHigginsLee_score_rhythm)
        LonguetHigginsLeeOriginalScores_list.append(original_LonguetHigginsLee_score_rhythm)
        PressingVelocityScores_list.append(velocity_Pressing_score_rhythm)
        PressingOriginalScores_list.append(original_Pressing_score_rhythm)
        WNBDVelocityScores_list.append(velocity_WNBD_score_rhythm)
        WNBDOriginalScores_list.append(original_WNBD_score_rhythm)
        OffBeatnessVelocityScores_list.append(velocity_OffBeatness_score_rhythm)
        OffBeatnessOriginalScores_list.append(original_OffBeatness_score_rhythm)
        IOIOriginalScores_list.append(original_IOI_score_rhythm)
        names_list.append(name)
    
    # Create Toussaint df
    Toussaint_scores_df = pd.DataFrame({'Rhythm': names_list, 
                                        'Original Toussaint': ToussaintOriginalScores_list,
                                        'Velocity Toussaint': ToussaintVelocityScores_list})
    
    # Create LHL df
    LonguetHigginsLee_scores_df = pd.DataFrame({'Rhythm': names_list, 
                                        'Original LHL': LonguetHigginsLeeOriginalScores_list,
                                        'Velocity LHL': LonguetHigginsLeeVelocityScores_list})
    
    # Create Pressing df
    Pressing_scores_df = pd.DataFrame({'Rhythm': names_list, 
                                        'Original Pressing': PressingOriginalScores_list,
                                        'Velocity Pressing': PressingVelocityScores_list})
    
    # Create WNBD df
    WNBD_scores_df = pd.DataFrame({'Rhythm': names_list, 
                                        'Original WNBD': WNBDOriginalScores_list,
                                        'Velocity WNBD': WNBDVelocityScores_list})
    
    # Create Off-Beatness df
    OffBeatness_scores_df = pd.DataFrame({'Rhythm': names_list, 
                                        'Original OffBeatness': OffBeatnessOriginalScores_list,
                                        'Velocity OffBeatness': OffBeatnessVelocityScores_list})
    
    # Create IOIstd df
    IOI_scores_df = pd.DataFrame({'Rhythm': names_list, 
                                  'Original IOIinformationEntropy': IOIOriginalScores_list,
                                  'Velocity IOIinformationEntropy': IOIOriginalScores_list})

    # Put all metrics dfs in a list
    metric_scores = [Toussaint_scores_df, LonguetHigginsLee_scores_df, Pressing_scores_df, WNBD_scores_df, OffBeatness_scores_df, IOI_scores_df]
    
    return metric_scores


# Def directories
directory_human = './metrics/sampled_rhythms/human'
directory_constant = './metrics/sampled_rhythms/constant'  


# Get human velocity rhythms scores
human_metric_scores =  compute_metric_score(directory_human)
Toussaint_H = human_metric_scores[0]
LHL_H = human_metric_scores[1]
Pressing_H = human_metric_scores[2]
WNBD_H = human_metric_scores[3]
OffBeatness_H = human_metric_scores[4]
IOI_informationEntropy_H = human_metric_scores[5]

# Save metric applied to human dfs
Toussaint_H.to_csv("./DataAnalysis/metric_scores/Toussaint_H.csv", index=False)
LHL_H.to_csv("./DataAnalysis/metric_scores/LHL_H.csv", index=False)
Pressing_H.to_csv("./DataAnalysis/metric_scores/Pressing_H.csv", index=False)
WNBD_H.to_csv("./DataAnalysis/metric_scores/WNBD_H2.csv", index=False)
OffBeatness_H.to_csv("./DataAnalysis/metric_scores/OffBeatness_H.csv", index=False)
IOI_informationEntropy_H.to_csv("./DataAnalysis/metric_scores/IOI_informationEntropy_H.csv", index=False)

# Get constant velocity rhythms scores
constant_metric_scores = compute_metric_score(directory_constant)
Toussaint_C = constant_metric_scores[0]
LHL_C = constant_metric_scores[1]
Pressing_C = constant_metric_scores[2]
WNBD_C = constant_metric_scores[3]
OffBeatness_C = constant_metric_scores[4]
IOI_informationEntropy_C = constant_metric_scores[5]

# Save metric applied to constant dfs
Toussaint_C.to_csv("./DataAnalysis/metric_scores/Toussaint_C.csv", index=False)
LHL_C.to_csv("./DataAnalysis/metric_scores/LHL_C.csv", index=False)
Pressing_C.to_csv("./DataAnalysis/metric_scores/Pressing_C.csv", index=False)
WNBD_C.to_csv("./DataAnalysis/metric_scores/WNBD_C2.csv", index=False)
OffBeatness_C.to_csv("./DataAnalysis/metric_scores/OffBeatness_C.csv", index=False)
IOI_informationEntropy_C.to_csv("./DataAnalysis/metric_scores/IOI_informationEntropy_C.csv", index=False)






