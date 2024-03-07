# Second Experiment - Polyphonic Rhythmic Pattern Measurement and Perception Investigation

A Study on the Effect of Dynamic Accents on the Perception and Measurement of Rhythm Complexity 

Polyphonic Patterns Experiment


This folder contains the data and the code used to investigate the perception and the possible measurement of complexity of polyphonic rhythmic patterns.
Here's a break down explanation of the content of this folder: 


- /Stimuli:         here you can find the audio stimuli included in the test

- /GMD:             this folder contains the original dataset of Groove Midi Dataset (/GMD/groove), from which the test stimuli were selected. Here you can also fin the code that was used to select the stimuli.

- /metrics:         in this directory you can find the polyphonic complexity metrics class definition, as well as the script that was used to compute the metric scores of the selected patterns.

- /public:          this folder contains all the files that were necessary for the website definition

- /output:          here the test results are stored in a json format

- /DataAnalysis:    this is the folder where all the analysis is conducted: test scores distribution, correlation between test data and metric scores, linear regression models, scatter and violin plots, and finally distribution of velocity mode differences in perception