import numpy as np
import math
import itertools

def get_pattern(length, onsets_indeces) :

    # This function obtains the pattern as a sequence of 0 and 1 
    # given the length of the pattern and the positions of its onsets

    pattern = np.zeros(length)
    for i in range(length):
        if i in onsets_indeces : 
            pattern[i] = 1
        else :
            pattern[i] = 0
    pattern = pattern.astype(int)
    return(pattern)

def get_pattern_with_velocities(length, onsets_indeces, onsets_velocities) :

    # This function obtains the pattern as a sequence of values between 0 and 1 (the value of each element represents its normalized velocity)
    # given the length of the pattern, the positions of its onsets and the velocity of each onset

    pattern = np.zeros(length)
    for i in range(length):
        if i in onsets_indeces : 
            index = np.where(onsets_indeces==i)
            pattern[i] = onsets_velocities[index]
        else :
            pattern[i] = 0
    pattern = pattern.astype(float)
    return(pattern)


def prime_factors(n):

    # Get the factorization in one vector with all the factors
    i = 2
    all_factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            all_factors.append(i)
    if n > 1:
        all_factors.append(n)

    # Represent the factors with two vectors, one for the unique factors and one telling how many times they are repeated
    unique_factors = np.array(list(set(all_factors)))
    pow = np.zeros(len(unique_factors)).astype(int)
    for i in range(len(unique_factors)):
        pow[i] = all_factors.count(unique_factors[i])

    return unique_factors, pow
    


def lcm(a,b):                           # computes the Least Common Multiple
  return (a * b) // math.gcd(a,b)


def next_power_of_2(x):
    return 1 if x == 0 else 2**math.floor(math.log2(x))


def subsample_velocities(pattern_velocities, quantization_levels):

    # This function takes a pattern where there are velocities to express the onsets 
    # and reduces the range of values that those onsets can have 
    # it is useful in the velocity adaptation of Lempel Ziv Coding, to keep controlled the vocabulary dimension

    values = np.linspace(0,1,quantization_levels)
    print('Velocity quantization levels are: ', values)
    subsampled_pattern = np.zeros(len(pattern_velocities))
    
    for i in range(len(pattern_velocities)):
        subsampled_pattern[i] = round(min(values, key=lambda x: abs(pattern_velocities[i] - x)),2)

    return subsampled_pattern

def check_window(window, vocabulary):           # window is an array, vocabulary a list of arrays
    
    # This function is used for the Lempel Ziv Coding algorithm
    # it checks if the word in the current window can be generated from the so far obtained vocabulary of words
    # if it returns True, the word won't be added to the vocabulary, otherwise it will

    len_win = len(window)
    vocab_elements = len(vocabulary)
    
    if vocab_elements != 0: 

        # first condition                                   # if the window q is contained in the vocabulary concatenation
        tot_vocab = np.concatenate(vocabulary, axis=0)
        for i in range(len(tot_vocab) - len_win+1):
            if np.array_equal(tot_vocab[i:i+len_win], window): 
                return True

        # second condition                                  # if all elements of window q are equal to the last element in vocabulary
        if ((np.all(window == window[0])) & (window[0] == tot_vocab[-1])):
            return True
        
        # third condition                               # if there is a sequence in vocabulary's end whose repetition makes window q                     
        sequence_lenghts = range(2, len(window)//2+1)
        for length in sequence_lenghts:
            if len(window) % length == 0:
                sequence = tot_vocab[:-length]
                repeated = np.tile(sequence, len(window) // length)
                
                if np.array_equal(repeated, window): return True

    return False


def get_IOI_frequencies(length, onsets_indeces):

    # This function computes the IOIs for a rhythmic pattern 
    # Takes as argument the length and the indeces of the onsets in the pattern
    # and returnes as output the global and local frequencies for each bin (each representing an IOI value)
    # The frequencies array have same length as the input array, in this way all possible bins are considered, 
    # and the output arrays can be used to generate a probability distribution

    # Global IOIs
    global_ioi = []
    for i in range(len(onsets_indeces)):     
        distance = abs(onsets_indeces[i] - (length + onsets_indeces[0])) \
                if (i == len(onsets_indeces)-1) else abs(onsets_indeces[i] - onsets_indeces[i+1])
        interval = distance if (len(onsets_indeces==1)) else min(distance, length-distance)
        global_ioi.append(interval)

    global_frequencies = np.bincount(np.array(global_ioi), minlength=length)
    
    # Local IOIs
    local_ioi = []        
    for i in range(len(onsets_indeces)):
        if len(onsets_indeces)==1: 
            interval = length
            local_ioi.append(interval)
        else:
            for j in range(len(onsets_indeces) - i-1):
                distance = abs(onsets_indeces[i]-onsets_indeces[i+j+1])
                interval = min(distance, length-distance)
                local_ioi.append(interval)

    local_frequencies = np.bincount(np.array(local_ioi), minlength=length)

    return global_frequencies, local_frequencies

def get_runs(previous_level):

    # This function is used in the CEPS algorithm
    # it takes as input a representation of the pattern and outputs a new, more compressed representation 
    # where the elements are runs of consecutive elements in the previous configuration

    new_level = []
    for group in itertools.groupby(previous_level):
            run = (list(group[1]))
            new_level.append(run)
    return new_level

def get_ditribution(level):

    # This function is used in the CEPS algorithm
    # it takes as input a representation of the pattern and outputs its probability distribution

    distribution = []
    counted = []
    for i in range(len(level)):
        if level[i] not in counted:            
            counted.append(level[i])
            count = 0
            for j in range(len(level)):
                element1 = np.array(level[i], dtype=object)
                element2 = np.array(level[j], dtype=object)
                if np.shape(element1)==np.shape(element2):
                    if np.equal(element1, element2).all():
                        count += 1
            distribution.append(count)
    distribution = [x / len(level) for x in distribution]
    return distribution

def get_composites(previous_level):

    # This function is used in the CEPS algorithm
    # it takes as input a representation of the pattern and outputs a new, more compressed representation
    # where the elements are composites of the consecutive elements of the previous representation 

    min_composite = 20
    for i in range(len(previous_level)):            # i is the offset, this is done to find the configuration with the smallest n° of composites
        composite = []
        rearranged_sequence = previous_level[i:] + previous_level[:i]
        for j in range(0, len(rearranged_sequence)-1, 2):
            new_elem = rearranged_sequence[j] + rearranged_sequence[j+1]
            composite.append(new_elem)
        if(len(composite)<min_composite): 
            min_composite=len(composite)
            offset = i
            new_level = composite
    return new_level

def entropy(level_distribution, lengths_distribution):

    # This function computes the maximum uncertainty of 4 random variables, 
    # with the assumption that each of these is uncorrelated

    H_x = 0
    for i in range(len(level_distribution)):
        if level_distribution[i] != 0:
            H_x -= level_distribution[i]*math.log2(level_distribution[i])
    H_y = 0
    for i in range(len(lengths_distribution)):
        if lengths_distribution[i] != 0:   
            H_y -= lengths_distribution[i]*math.log2(lengths_distribution[i])
    H_max_level = 2* (H_x + H_y)

    return(H_max_level)



# Function to create scores dataframe
def get_scores(df):
    scores = df.iloc[:, 6:126]
    scores.columns = scores.columns.str[-3:]
    scores = scores.reindex(sorted(scores.columns), axis=1)          # sort numerically the rhythms

    # Turn strings into numerical scores to use histplot
    vote_mapping = {
        'Very low': 1,
        'Low': 2,
        'Medium': 3,
        'High': 4,
        'Very high': 5
    }
    scores = scores.applymap(lambda x: vote_mapping.get(x, np.nan))
    return scores