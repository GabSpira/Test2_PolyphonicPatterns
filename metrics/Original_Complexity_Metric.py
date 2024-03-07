import numpy as np
import math
from metrics.ComplexityMetricsFunctions import get_pattern, check_window, get_IOI_frequencies


#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-. ORIGINAL METRICS CLASS -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.#

# This is the class with the original version (not considering velocity) of the considered metrics

#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.#


class Original_Complexity_Metric_Class:

    def __init__(self, length, onsets_indeces):
        self.length = length
        self.onsets_indeces = onsets_indeces

    def __str__(self):
        return f"{self.length}({self.onsets_indeces})"
    
    def getToussaintComplexity(self):
        
        # print('\n\n### ORIGINAL TOUSSAINT ###')

        # Build hierarchy
        levels = int(math.log2(self.length))+1
        weights = np.zeros(self.length)
        for level in range(levels) :
            step = pow(2,level)
            weights[0:16:step] += 1
        # print('The pattern has length equal to ', self.length, ', so the relative hierarchy is: ', weights)

        # Obtain non-normalized complexity score (metricity, inversely proportional to actual complexity)
        onset_weights = weights[self.onsets_indeces]
        metricity = sum(onset_weights)
        # print('The relative metricity (inversely proportional to the complexity) is: ', metricity)

        # Obtain complexity (Onset Normalization) 
        n = (self.onsets_indeces).shape[0]                      #n° of onsets in the pattern
        n_sorted_weights = np.argsort(weights)[::-1][:n]
        max_metricity = sum(weights[n_sorted_weights])

        complexity_Toussaint_OnsetNorm = max_metricity - metricity
        # print('The onset normalized Toussaint complexity score is: ', complexity_Toussaint_OnsetNorm)

        return(complexity_Toussaint_OnsetNorm)
    


    def getLonguetHigginsLeeComplexity(self):
        
        print('\n\n### ORIGINAL LONGUET-HIGGINS & LEE ###')

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
        pattern = get_pattern(self.length, self.onsets_indeces)

        # Find syncopations
        syncopations = []
        check = -10
        for i in range(self.length):
            if pattern[i] == 0:              #for all silences
                if weights[i]>check:            #if they have greater weight then the previous one (in case there has been syncopation)
                    search_zone = list(range(i-1, -1, -1)) + list(range(self.length-1, i, -1))
                    for j in search_zone:
                        if ((pattern[j] != 0) & (weights[i]>weights[j])):   #if there's an onset with lower weight
                            s = weights[i]-weights[j]
                            if s>0:                          #and it is situated before of the silence
                                syncopations.append(s)              #then there has been a syncopation
                            break
                check = weights[i]
        syncopations = np.array(syncopations)
        print(syncopations)

        # Complexity score
        complexity_LonguetHiggindLee = sum(syncopations) 
        print('The Longuet-Higgins & Lee complexity score is: ', complexity_LonguetHiggindLee)

        return(complexity_LonguetHiggindLee)
    


    def getPressingComplexity(self):

        print('\n\n### ORIGINAL PRESSING ###')

        # Pattern initialization 
        pattern = get_pattern(self.length, self.onsets_indeces)
        
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
            weights = np.zeros(m).astype(int)            
            for j in range(m):                          # for each sub-rhythm find the associate weight
                sub_rhythm = chunks[j,:]
                next_sub_rhythm = chunks[j+1,:] if j+1<m else chunks[0,:]
                pulses = sub_rhythm[0::int(n/2)]
                offbeats = sub_rhythm[1::int(n/2)]
                offbeats_2 = np.concatenate((sub_rhythm[1:int(n/2):2], sub_rhythm[int(n/2)+1:n:2]))

                weight_null, weight_filled, weight_run, weight_upbeat, weight_syncop = 0,0,0,0,0

                # NULL (no onset, or only the first pulse)
                if all(element == 0 for element in sub_rhythm[1:]): 
                    weight_null = 0             

                # FILLED (onset on each pulse)                                                  
                if all(element != 0. for element in pulses):                                    
                    weight_filled =  1#/(np.mean(pulses))

                # RUN (onset on first pulse + a sequence (only 2 in Pressing paper))            
                if (((pulses[0]!=0.) & (offbeats[0]!=0.)) or ((pulses[1]!=0.) & (offbeats[1]!=0.))):
                    weight_run = 2 

                # UPBEAT (onset on last pulse and first of next subrhythm)                      
                if ((sub_rhythm[-1]!=0.) & (next_sub_rhythm[0]!=0.)):
                    weight_upbeat = 3 
                    
                # SYNCOPATION (onset off-beat)                                                  
                if any(element!=0. for element in offbeats_2):                                  
                    if pulses[0]==0.: weight_syncop = 5   
                    if pulses[1]==0.: weight_syncop = 5   
                    if ((pulses[0]!=0)&(pulses[1]!=0)): break 
                
                weights[j] = max(weight_null, weight_filled, weight_run, weight_upbeat, weight_syncop)

                # print('metrical level: ', i+1, ', chunk number ', j, ': ', sub_rhythm) 
                # print(weights[j])
            
            avg[i] = np.sum(weights)/m
            # print('avg:', avg[i])

        complexity_Pressing = np.sum(avg)   

        print('The Pressing complexity score is: ', complexity_Pressing)

        return(complexity_Pressing)
    


    def getWeightedNotetoBeatDistance(self):
        
        print('\n\n### ORIGINAL WEIGHTED NOTE TO BEAT DISTANCE ###')

        # Meter initialization - intended by default for 16-length rhythms
        meter4_indeces_2bars = [0,4,8,12,16,20,24,28]
        sum_weights = 0

        # For each onset compute the weights depending on the distance from the nearest beat and the following ones
        for i in range(len(self.onsets_indeces)):
            
            # define the considered onset
            x = self.onsets_indeces[i]                          # index of the considered onset in the pattern array
            
            # define the smaller distance from a beat and its index
            d = np.min(abs(meter4_indeces_2bars - x))              # n° of onsets btw the considered onset and the nearest beat
            # T = d/len(meter4_indeces_2bars)                        # actual distance
            T = d

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

            sum_weights = sum_weights + D

        # Complexity score
        complexity_WNBD = sum_weights/len(self.onsets_indeces)     
        print('The Weighted Note to Beat Distance complexity score is: ', complexity_WNBD)

        return(complexity_WNBD) 
    

    def getStandardDeviationComplexity(self):

        print('\n\n### IOI - STANDARD DEVIATION ###')

        # Get IOI frequencies, both global and local
        global_frequencies, local_frequencies = get_IOI_frequencies(self.length, self.onsets_indeces)

        # Compute Standard Deviation - global IOIs
        std_global = np.std(global_frequencies)

        # Compute Standard Deviation - local IOIs
        std_local = np.std(local_frequencies)

        # Compute complexities as inversely proportional to STDs
        complexity_STD_globalIOI = 1/std_global
        complexity_STD_localIOI = 1/std_local
        print('The global IOIs Standard Deviation complexity score is: ', complexity_STD_globalIOI)
        print('The local IOIs Standard Deviation complexity score is: ', complexity_STD_localIOI)
        
        return complexity_STD_globalIOI, complexity_STD_localIOI
    
    def getInformationEntropyComplexity(self):

        print('\n\n### IOI - INFORMATION ENTROPY ###')

        # Get IOI frequencies, both global and local
        global_frequencies, local_frequencies = get_IOI_frequencies(self.length, self.onsets_indeces)
        
        # Compute probability distributions
        global_pdf = global_frequencies/np.sum(global_frequencies)
        local_pdf = local_frequencies/np.sum(local_frequencies)

        # Compute entropies
        H_global = 0
        for i in range(len(global_pdf)):
            if global_pdf[i] != 0:
                H_global -= global_pdf[i]*math.log2(global_pdf[i])
        H_local = 0
        for i in range(len(local_pdf)):
            if local_pdf[i] != 0:
                H_local -= local_pdf[i]*math.log2(local_pdf[i])

        # Complexities
        complexity_InformationEntropy_globalIOI = H_global
        complexity_InformationEntropy_localIOI = H_local
        print('The global IOIs Information Entropy complexity score is: ', complexity_InformationEntropy_globalIOI)
        print('The local IOIs Information Entropy complexity score is: ', complexity_InformationEntropy_localIOI)
        
        return complexity_InformationEntropy_globalIOI, complexity_InformationEntropy_localIOI
    
    
    def getTallestBinComplexity(self):

        print('\n\n### IOI - TALLEST BIN ###')

        # Get IOI frequencies, both global and local
        global_frequencies, local_frequencies = get_IOI_frequencies(self.length, self.onsets_indeces)

        # Compute probability distributions
        global_pdf = global_frequencies/np.sum(global_frequencies)
        local_pdf = local_frequencies/np.sum(local_frequencies)     

        # Find the max in each distribution
        global_max = np.max(global_pdf)
        local_max = np.max(local_pdf)

        # Compute the complexities 
        complexity_TallestBin_globalIOI = 1/global_max
        complexity_TallestBin_localIOI = 1/local_max

        print('The global IOIs Tallest Bin complexity score is: ', complexity_TallestBin_globalIOI)
        print('The local IOIs Tallest Bin complexity score is: ', complexity_TallestBin_localIOI)

        return(complexity_TallestBin_globalIOI, complexity_TallestBin_localIOI)

    


    def getLempelZivCodingComplexity(self):

        print('\n\n### ORIGINAL LEMPEL-ZIV CODING ###')

        # Variables initialization
        s = []                                              # vocabulary
        r = get_pattern(self.length, self.onsets_indeces)   # pattern
        r = np.concatenate((r,r))                           # 2 iterations
        j = 0                                               # window start
        i = 0                                               # window end
        
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
        complexity_LempelZiv = len(s)     
        print('The Lempel Ziv complexity score is: ', complexity_LempelZiv)

        return complexity_LempelZiv
    

    def getOffBeatnessComplexity(self):

        print('\n\n### ORIGINAL TOUSSAINT OFF-BEATNESS ###')
        
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
            if i in off_beat_indeces: complexity_OffBeatness += 1

        print('The Off-Beatness complexity score is: ', complexity_OffBeatness)

        return(complexity_OffBeatness)
    
