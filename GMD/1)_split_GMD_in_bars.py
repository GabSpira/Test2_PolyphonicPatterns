import pretty_midi
import os
import numpy as np
import math
import copy


#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-. SPLIT GROOVE MIDI DATASET IN BARS -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.#

# Run this script to inspect all GMD folders, split each pattern in bars, and save all splitted bars in a single folder 

#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-#


directory = './GMD/groove/'
Toussaint_all_scores=[]
tot_number_of_patterns = []
discarded_patterns = []


for sub in os.listdir(directory):
    subdir = os.path.join(directory, sub)
    if os.path.isdir(subdir):
        for sub2 in os.listdir(subdir):
            subdir2 = os.path.join(subdir, sub2)
            if os.path.isdir(subdir2):
                
                for file in os.listdir(subdir2):

                    # Def midi object path
                    path = os.path.join(subdir2, file)
                    name_ext = os.path.basename(path)
                    name = os.path.splitext(name_ext)[0]

                    # Discard files that are not in 4/4
                    time_signature = (name.split('_')[4])
                    if time_signature!='4-4':
                        discarded_patterns.append(path)
                        continue
                    
                    # Def current midi object
                    pm = pretty_midi.PrettyMIDI(path)

                    # Get metric grid information 
                    BPM = int(name.split('_')[2])
                    bar_duration = 60/BPM * 4                   #bar (in seconds)
                    # twobars_duration = bar_duration*2           #2 bars (in seconds)
                    resolution = 1/16                           #sixteenth note 
                    tatum = bar_duration*resolution             #resolution note (in seconds)
                    length = int(bar_duration/tatum)            #16 (in cells)

                    # Quantize to resolution
                    midi_duration = pm.instruments[0].notes[-1].end     # in seconds
                    quantized_grid = np.arange(0, midi_duration, tatum)
                    for note in pm.instruments[0].notes:
                        quantized_start = min(quantized_grid, key=lambda x: abs(note.start - x))
                        note.start = quantized_start

                    # Get number of bars in midi file
                    n_bars = math.ceil(midi_duration/bar_duration)
                    bars = np.arange(0, (n_bars+1)*bar_duration, bar_duration)

                    # Isolate each bar in midi file
                    for i in range(n_bars):

                        # Create a copy of the original midi that will be reduced to the single bar
                        current_bar_midi = copy.deepcopy(pm)

                        # Def current bar
                        bar_interval = [bars[i], bars[i+1]]                               

                        # Collect notes outside the bar
                        notes_to_remove = []
                        for note in current_bar_midi.instruments[0].notes:
                            if not(bar_interval[0] <= note.start < bar_interval[1]):     
                                notes_to_remove.append(note)

                        # Collect events outside the bar
                        events_to_remove = []
                        for event in current_bar_midi.instruments[0].control_changes:       
                            if not(bar_interval[0] < event.time < bar_interval[1]):     
                                events_to_remove.append(event)

                        # Remove collected outside of the bar notes and events
                        for note in notes_to_remove:
                            current_bar_midi.instruments[0].notes.remove(note)
                        for event in events_to_remove:
                            current_bar_midi.instruments[0].control_changes.remove(event)

                        # Place bar notes to the first bar position
                        for note in current_bar_midi.instruments[0].notes:
                            note.start = note.start-bar_interval[0]
                            note.end = note.end-bar_interval[0]
                            if note.end >= bar_duration: note.end=bar_duration-0.001

                        # Place bar events to the first bar position
                        for event in current_bar_midi.instruments[0].control_changes:
                            event.time = event.time-bar_interval[0]

                        # Write the sinle bar midi file
                        current_bar_midi.write(f'./GMD/GMD_splitted_bars/{name}_bar_{i+1}.mid')




# # Count splitted bars
# count = 0
# for file in os.listdir('./data/GMD_splitted_bars'):
#     count += 1 

# print(count)

                    



