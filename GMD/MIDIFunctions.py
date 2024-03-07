import pretty_midi
import numpy as np
import mir_eval.display
import librosa.display
import matplotlib.pyplot as plt



def plot_beats(pm, start_pitch, end_pitch, fs=7000, fixed_duration=2):
    
    # Figure settings
    plt.figure(figsize=(10,4))
    plt.axes().set_facecolor('black')
    
    # Plot the pattern
    librosa.display.specshow(pm.get_piano_roll(fs)[start_pitch:end_pitch],
                             hop_length=1, sr=fs, x_axis='time', y_axis ='cqt_note',
                             fmin=pretty_midi.note_number_to_hz(start_pitch))
    
    # Figure limits
    ymin, ymax = plt.ylim()
    plt.xlim(-0.5,2.5)
    
    # Get beats and downbeat times
    downbeats = pm.get_beats()
    downbeats = np.append(downbeats, fixed_duration)
    beats = np.interp(np.arange(downbeats.shape[0]*4), np.arange(1, downbeats.shape[0]*4, 4), downbeats)
    
    # Plot beats as grey lines, downbeats as white lines
    mir_eval.display.events(beats, base=ymin, height=ymax, color='#AAAAAA')
    mir_eval.display.events(downbeats, base=ymin, height=ymax, color='#FFFFFF', lw=2)
    
    # Plot
    plt.show()



def get_velocities(onsets_times, pm):

    velocities = []
    for onset in onsets_times:

        closest_note = None
        closest_distance = float('inf')
        
        for note in pm.instruments[0].notes:  # Considera solo il primo strumento (batteria monofonica)
            note_distance = abs(note.start - onset)
            if note_distance < closest_distance:
                closest_note = note
                closest_distance = note_distance
        
        if closest_note is not None:
            velocity = closest_note.velocity
            # print(f"Velocità della nota più vicina all'onset {onset}: {velocity}")
        else:
            print(f"Nessuna nota trovata per l'onset {onset}")

        velocities.append(velocity)

    onsets_velocities = np.array(velocities)
    onsets_velocities = onsets_velocities/127
    # print("The onsets have velocities: ", onsets_velocities)

    return onsets_velocities