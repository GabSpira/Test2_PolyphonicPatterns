import pretty_midi
from Velocity_Complexity_Metric import Velocity_Complexity_Metric_Class
from Original_Complexity_Metric import Original_Complexity_Metric_Class
from UtilityFunctions import get_pattern_with_velocities, get_pattern
from MIDIFunctions import get_velocities
import numpy as np
import os
import pandas as pd


#-.-.-.-.-.-.-.-.-.-.-.-.--.-.-.-.-. COMPUTE TOUSSAINT ON GMD BARS -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.#

# Run this script to preprocess each of the splitted bars of GMD by applying GROOVAE's reduction mapping, 
# Mezza's reduction rules and to compute the complexity scores of each according to Polyphonic Toussaint

#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-#



directory = './GMD/GMD_splitted_bars'

count = 0       
for file in os.listdir(directory):
    count += 1
print(f"There are {count} bars among which one can choose")

# Init lists
velocity_Toussaint_all_scores=[]
original_Toussaint_all_scores=[]
all_rhythms = []
all_rhythms_reduced = []
velocity_var = []
velocity_var_groups_mean = []

for file in os.listdir(directory):

    # Def midi object
    path = os.path.join(directory, file)
    pm = pretty_midi.PrettyMIDI(path)

    # Get BPM from file name
    name_ext = os.path.basename(path)
    name = os.path.splitext(name_ext)[0]
    BPM = int(name.split('_')[2])

    # Get metric grid information from BPM
    bar_duration = 60/BPM * 4                       #bar (in seconds)
    resolution = 16
    tatum = bar_duration/resolution                 #16th note (in seconds)
    length = int(bar_duration/tatum)                #16 (in cells)

    # Reduction Mapping from GROOVAE
    if pm.instruments != []:
        for note in pm.instruments[0].notes:
            pitch=note.pitch
            if pitch in [37, 38, 40]: note.pitch = 38           # types of snares
            if pitch in [47, 48]: note.pitch = 48               # toms
            if pitch in [43, 45, 58]: note.pitch = 45           # lo toms
            if pitch in [46, 26]: note.pitch = 46               # hh open
            if pitch in [42, 22, 44]: note.pitch = 42           # hh closed
            if pitch in [49, 52, 55, 57]: note.pitch = 49       # crashes
            if pitch in [51, 59, 53]: note.pitch = 51           # rides

    # Apply Mezza Reduction Rules (at least 3 instruments, at least 4 notes)
    if pm.instruments!=[]: 
        number_pitches = []
        onset_times = []
        for note in pm.instruments[0].notes:
            if note.pitch not in number_pitches: number_pitches.append(note.pitch)
            if note.start not in onset_times: onset_times.append(note.start)
        if len(number_pitches)<3: continue
        if len(onset_times)<4: continue
    else: continue

    # Save reduced midi   
    pm.write(f'./GMD/GMD_reduced_bars/{name}_reduced.mid')

    # Collect velocity variance mean over all notes in midi file
    np.seterr(invalid='ignore')
    if ((len(pm.instruments)!=0) ): #& (len(pm.instruments[0].notes))):
        velocities = [pm.instruments[0].notes[i].velocity for i in range(len(pm.instruments[0].notes))]
        velocity_var.append(np.var(np.array([velocities])))
    else: velocity_var.append(0)

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
    groups_metric_scores_velocity = []
    groups_metric_scores_original = []
    velocity_var_groups = []

    for i in range(len(separated_instruments)):

        # Def pretty midi object
        pm_group = separated_instruments[i]

        # Get onsets
        onsets_times_group = pm_group.get_onsets()
        onsets_indeces_group = np.unique((onsets_times_group/tatum).astype(int))            # exclude multiple notes at the same time (due to quantization)
        onsets_times_group = onsets_indeces_group*tatum
        
        # Get velocities
        onsets_velocities_group = get_velocities(onsets_times_group, pm_group)

        # Collect var info
        if onsets_velocities_group.size > 0:
            var_group = np.var(onsets_velocities_group)
        velocity_var_groups.append(var_group)

        # Get pattern 
        pattern = get_pattern_with_velocities(length, onsets_indeces_group, onsets_velocities_group)

        # Def metric for group
        metrics_velocity = Velocity_Complexity_Metric_Class(length, onsets_indeces_group, onsets_velocities_group)
        metrics_original = Original_Complexity_Metric_Class(length, onsets_indeces_group)

        # Compute metrics (both original and velocity algorithms)
        group_metric_velocity = metrics_velocity.getToussaintComplexity_Velocity()
        group_metric_original = metrics_original.getToussaintComplexity()

        # Def weight according to group 
        # w = 1/(i+1)
        w = 1
        
        # Apply weight to metrics
        weighted_group_metric_velocity = group_metric_velocity*w
        weighted_group_metric_original = group_metric_original*w

        # Collect group metrics
        groups_metric_scores_velocity.append(weighted_group_metric_velocity)
        groups_metric_scores_original.append(weighted_group_metric_original)

    # Get Toussaint score for that pattern
    velocity_Toussaint_score_rhythm = sum(groups_metric_scores_velocity)
    original_Toussaint_score_rhythm = sum(groups_metric_scores_original)

    # Collect mean velocity var over all instruments
    if len(velocity_var_groups)!=0:
        velocity_var_groups_mean.append(np.sum(velocity_var_groups)/len(velocity_var_groups))
    else: velocity_var_groups.append(0)

    # Collect rhythm info in lists to build a df
    velocity_Toussaint_all_scores.append(velocity_Toussaint_score_rhythm)
    original_Toussaint_all_scores.append(original_Toussaint_score_rhythm)
    all_rhythms.append(name)
    all_rhythms_reduced.append(name + '_reduced')





# Create and save df with 2 columns: each row is a rhythm, indicated by name and score            
rhythms_score = pd.DataFrame({'Rhythm': all_rhythms, 'Velocity Score': velocity_Toussaint_all_scores, 'Original Score': original_Toussaint_all_scores})
rhythms_score.to_csv("./GMD/all_rhythms_score.csv", index=False)

rhythms_score_reduced = pd.DataFrame({'Rhythm': all_rhythms_reduced, 'Original Score': original_Toussaint_all_scores, 'Var1':velocity_var, 'Var2': velocity_var_groups_mean})
rhythms_score_reduced.to_csv("./GMD/all_rhythms_score_reduced.csv", index=False)

print('Rhythms scores dataframe correctly saved!')









