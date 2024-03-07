import numpy as np
import math
from UtilityFunctions import check_window, subsample_velocities, get_pattern_with_velocities



#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-. VELOCITY METRICS CLASS -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.#

# This is the class with the velocity version (considering velocity) of the considered metrics

#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.#



class Velocity_Complexity_Metric_Class:

    def __init__(self, length, onsets_indeces, onsets_velocities):
        self.length = length
        self.onsets_indeces = onsets_indeces
        self.onsets_velocities = onsets_velocities

    def __str__(self):
        return f"{self.length}({self.onsets_indeces})"
    
    
    def getToussaintComplexity_Velocity(self):                          
        
        # This function computes the including-the-velocity version of the Toussaint metric
        # the adaptation is based on the intuition that the max metricity for pattern depends on the sorted velocities of the pattern
        
        # print('\n\n### VELOCITY TOUSSAINT ###')

        # Build hierarchy
        levels = int(math.log2(self.length))+1
        weights = np.zeros(self.length)
        for level in range(levels) :
            step = pow(2,level)
            weights[0:self.length:step] += 1
        # print('The pattern has length equal to ', self.length, ', so the relative hierarchy is: ', weights)

        # Obtain non-normalized complexity score (metricity, inversely proportional to actual complexity)
        onset_weights = weights[self.onsets_indeces]

        # Multiply weights of the onsets for the velocities of the onsets
        weights_times_velocities = np.multiply(onset_weights, self.onsets_velocities)
        vel_metricity = sum(weights_times_velocities)
        # print('The velocity-weighted metricity is ', vel_metricity)

        # sort highest weights to compute max metricity 
        n = (self.onsets_indeces).shape[0]                         #n° of onsets in the pattern
        n_sorted_weights_indeces = np.argsort(weights)[::-1][:n]
        n_sorted_weights = weights[n_sorted_weights_indeces]

        # mulitply the max weights for the sorted pattern velocities to obtain max metricity
        n_sorted_velocities = np.sort(self.onsets_velocities)[::-1]
        highest_weights_sorted_velocities = np.multiply(n_sorted_weights, n_sorted_velocities)
        max_metricity = sum(highest_weights_sorted_velocities)

        # ONSET NORMALIZATION
        Complexity_Velocity_Toussaint_OnsetNorm = max_metricity - vel_metricity
        # print('The onset normalized Toussaint complexity score is: ', Complexity_Velocity_Toussaint_OnsetNorm)

        return(Complexity_Velocity_Toussaint_OnsetNorm)
    

    def getLonguetHigginsLeeComplexity_Velocity(self):
        
        print('\n\n### VELOCITY LONGUET-HIGGINS & LEE ###')

        # Build hierarchy
        levels = int(math.log2(self.length))+1
        weights = np.zeros(self.length)
        for level in range(levels) :
            step = pow(2,level)
            for i in range(1,self.length):
                if i%step != 0:
                    weights[i] -= 1
        print('The pattern has length equal to ', self.length, ', so the relative hierarchy is: ', weights)
        
        # Build pattern
        pattern = get_pattern_with_velocities(self.length, self.onsets_indeces, self.onsets_velocities)

        # Find syncopations
        syncopations = []
        check = -10
        for i in range(self.length):
            # SYNCOPATIONS:
            # IF SILENCE WITH HIGHER WEIGHT AFTER ONSET WITH LOWER WEIGHT
            if pattern[i] == 0:              #for all silences
                if weights[i]>check:
                    search_zone = list(range(i-1, -1, -1)) + list(range(self.length-1, i, -1))
                    for j in search_zone:
                        if ((pattern[j] != 0) & (weights[i]>weights[j]) & (pattern[i]<pattern[j])):   #if there's an onset with lower weight and eventually higher velocity
                            s = weights[i]-weights[j]
                            if s>0:                                                     #and it is situated before of the silence                      
                                v = s * (1 - (np.std([pattern[j], pattern[i]])) )         #syncopation weighted by a measure of velocity difference
                                syncopations.append(v)                                  #then there has been a syncopation
                            break
                check = weights[i]
           
        syncopations = np.array(syncopations)
        print(syncopations)
        
        # Complexity score
        complexity_Velocity_LonguetHigginsLee = sum(syncopations) 
        print('The Longuet-Higgins & Lee complexity score is: ', complexity_Velocity_LonguetHigginsLee)

        return(complexity_Velocity_LonguetHigginsLee)
    

    def getPressingComplexity_Velocity(self):

        print('\n\n### VELOCITY PRESSING ###')

        # Pattern initialization 
        pattern = get_pattern_with_velocities(self.length, self.onsets_indeces, self.onsets_velocities)

        # Get chunks of the pattern - by default intended for binary patterns
        chunk_dimensions = np.zeros(math.ceil(math.log2(self.length))).astype(int)
        metrical_levels = len(chunk_dimensions)-1
        for i in range(metrical_levels):
            chunk_dimensions[i] = int(self.length/math.pow(2, i))
            i +=1
        
        # Get the complexity as the sum of the averages of the chunk weights obtained in each metrical level
        avg = np.zeros(metrical_levels)
        for i in range(metrical_levels): 
            chunks = np.reshape(pattern, (-1, chunk_dimensions[i]))
            m,n = chunks.shape                          # The pattern is divided in m slices (sub-rhythms) of length n
            weights = np.zeros(m).astype(float)            
            for j in range(m):                          # for each sub-rhythm find the associate weight
                sub_rhythm = chunks[j,:]
                next_sub_rhythm = chunks[j+1,:] if j+1<m else chunks[0,:]
                pulses = sub_rhythm[0::int(n/2)]
                offbeats = sub_rhythm[1::int(n/2)]
                offbeats_2 = np.concatenate((sub_rhythm[1:int(n/2):2], sub_rhythm[int(n/2)+1:n:2]))

                weight_null, weight_filled, weight_run, weight_upbeat, weight_syncop = float(0),float(0),float(0),float(0),float(0)
                
                # NULL (no onset, or only the first pulse)
                if all(element == 0. for element in sub_rhythm[1:]): 
                    weight_null = 0.             

                # FILLED (onset on each pulse)                                                  # if pulse has lower velocity -> more complex 
                if all(element != 0. for element in pulses):                                    # if greater difference in 2 onsets -> more complex
                    weight_filled =  1 - math.sqrt( np.std([pulses[1],pulses[0]]) * (np.mean(pulses)) )

                # RUN (onset on first pulse + a sequence (only 2 in Pressing paper))            # if offbeat has higher velocity then pulse -> more complex
                if ((pulses[0]!=0.) & (offbeats[0]!=0.)):
                    weight_run = 2 - math.sqrt( np.std([offbeats[0], pulses[0]]) )
                if ((pulses[1]!=0) & (offbeats[1]!=0)):
                    weight_run = 2 - math.sqrt( np.std([offbeats[1], pulses[1]]) )

                # UPBEAT (onset on last pulse and first of next subrhythm)                      # if offbeat has higher velocity then pulse -> more complex
                if ((sub_rhythm[-1]!=0.) & (next_sub_rhythm[0]!=0.)):
                    weight_upbeat = 3 - math.sqrt( np.std([sub_rhythm[-1], next_sub_rhythm[0]]) )
                    
                # SYNCOPATION (onset off-beat)                                                  # if offbeat has higher velocity -> more complex
                if any(element!=0. for element in offbeats_2):                                  # if lower level -> less complex 
                    if ((pulses[0]!=0)&(pulses[1]!=0)): break           # no pulse on the beat to have syncop
                    syncop = []
                    correction=0
                    if pulses[0]==0.: syncop.extend([elem for elem in offbeats_2[0:int(len(offbeats_2)/2)] if elem!=0])
                    if pulses[1]==0.: syncop.extend([elem for elem in offbeats_2[int(len(offbeats_2)/2):] if elem!=0])
                    if len(syncop)!=0: correction = np.std(syncop) / len(syncop) * (np.mean(syncop)) * (i+1)   
                    weight_syncop = 5 - math.sqrt( correction )       

                weights[j] = max(weight_null, weight_filled, weight_run, weight_upbeat, weight_syncop)

                # print('metrical level: ', i+1, ', chunk number ', j, ': ', sub_rhythm) 
                # print(weights[j])

            avg[i] = np.sum(weights)/m 
            # print('avg:', avg[i])

        complexity_Pressing_Velocity = np.sum(avg)   

        print('The Pressing complexity score is: ', complexity_Pressing_Velocity)

        return(complexity_Pressing_Velocity)
    


    def getWeightedNotetoBeatDistance_Velocity(self):
        
        print('\n\n### VELOCITY WEIGHTED NOTE TO BEAT DISTANCE ###')

        # Meter initialization - intended by default for 16-length rhythms
        meter4_indeces_2bars = [0,4,8,12,16,20,24,28]
        sum_weights = 0

        pattern = get_pattern_with_velocities(self.length, self.onsets_indeces, self.onsets_velocities)

        # For each onset compute the weights depending on the distance from the nearest beat and the following ones
        for i in range(len(self.onsets_indeces)):
            
            # define the considered onset
            x = self.onsets_indeces[i]                          # index of the considered onset in the pattern array
            
            # define the smaller distance from a beat and its index
            d = np.min(abs(meter4_indeces_2bars - x))              # n° of onsets btw the considered onset and the nearest beat
            T = d/len(meter4_indeces_2bars)                        # actual distance

            # define where the considered onset ends
            if i+1<len(self.onsets_indeces): 
                end = self.onsets_indeces[i+1]
            else: 
                end = self.length + self.onsets_indeces[0]
                
            # define the beats after the considered onset
            for k in range(len(meter4_indeces_2bars)):
                if meter4_indeces_2bars[k]>x: 
                    e1 = meter4_indeces_2bars[k]                   # first beat after the considered onset
                    e2 = meter4_indeces_2bars[k+1]                 # second beat after the considered onset
                    break            

            # assign weights based on the previous parameters
            if ((end <= e1) & (T!=0)):
                D = 1/T
            elif ((end <= e2)  & (T!=0)):
                D = 2/T
            elif ((e2 < end)  & (T!=0)):
                D = 1/T
            elif T==0: 
                D=0
            
            # weight taking account of velocity
            D = D*pattern[x]

            sum_weights = sum_weights + D

        # Complexity score
        complexity_WNBD_Velocity = sum_weights/len(self.onsets_indeces)     
        print('The Weighted Note to Beat Distance complexity score is: ', complexity_WNBD_Velocity)

        return(complexity_WNBD_Velocity) 
    
    
    def getLempelZivCodingComplexity_Velocity(self):

        print('\n\n### VELOCITY LEMPEL-ZIV CODING ###')

        # Variables initialization
        s = []                                              # vocabulary
        r = get_pattern_with_velocities(self.length, self.onsets_indeces, self.onsets_velocities)   # pattern
        r = np.concatenate((r,r))                           # 2 iterations
        j = 0                                               # window start
        i = 0                                               # window end
        n_levels = 5
        
        r = subsample_velocities(r, n_levels)
        print(r)

        # Build the vocabulary
        while (True):
            q = r[j:i+1]                                    #window  
            can_generate_q_from_s = check_window(q, s)
            if (can_generate_q_from_s == False): 
                s.append(q)
                i += 1
                j = i
            else: i += 1
            if i == (self.length * 2): break
        print('The pattern can be constructed from this vocabulary of sub-patterns: ', s)

        # Derive the complexity as the length of the vocabulary
        complexity_LempelZiv_Velocity = len(s)     
        print('The Lempel Ziv complexity score is: ', complexity_LempelZiv_Velocity)

        return complexity_LempelZiv_Velocity
    

    def getOffBeatnessComplexity_Velocity(self):

        print('\n\n### VELOCITY TOUSSAINT OFF-BEATNESS ###')

        # Get pattern with velocities
        pattern = get_pattern_with_velocities(self.length, self.onsets_indeces, self.onsets_velocities)
        
        # Find the possibly inscribible polygons
        polygon_vertices = []
        for i in range(2,self.length):
            if self.length%i==0: polygon_vertices.append(i)

        # Draw the polygons (mark the on-beat pulses)
        on_beat_indeces = []
        for i in polygon_vertices:
            for j in range(self.length):
                if ((j*i<self.length) & (j*i not in on_beat_indeces)):
                    on_beat_indeces.append(j*i)
        
        # Derive the off-beat pulses
        off_beat_indeces = np.setdiff1d(np.arange(self.length), on_beat_indeces)
        
        # Find the complexity as the number of onsets that are off-beat
        complexity_OffBeatness = 0
        for i in self.onsets_indeces:
            if i in off_beat_indeces: complexity_OffBeatness += pattern[i]

        print('The Off-Beatness complexity score is: ', complexity_OffBeatness)

        return(complexity_OffBeatness)
