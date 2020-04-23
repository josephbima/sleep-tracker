# -*- coding: utf-8 -*-
"""
This file is used for extracting features over windows of tri-axial accelerometer 
data. We recommend using helper functions like _compute_mean_features(window) to 
extract individual features.

As a side note, the underscore at the beginning of a function is a Python 
convention indicating that the function has private access (although in reality 
it is still publicly accessible).

"""

import numpy as np
from scipy.signal import find_peaks
import warnings

warnings.filterwarnings('ignore')


def _compute_mean_features(window):
    """
    Computes the mean x, y and z acceleration over the given window. 
    """
    return np.mean(window, axis=0)

# TODO: define functions to compute more features

def _compute_std_features(window):
    '''
    Computes the standard deviation of x, y and z acceleration over the given window

    Returns an array of numbers corresponding to the x, y and z values

    '''
    return np.std(window, axis = 0)

# def _compute_median(window):
#     return np.median(window, axis = 0) 

# def _compute_min(window):
#     return np.min(window)

def _compute_dominant_frequency(window):
    # Not Finished 
    return np.fft.rfft(window,axis=0).astype(float)[0]

def _compute_entropy_distribution(window):
    # Not Finished
    return np.histogram(window)

def _compute_magnitude(window):
    magnitude = []

    for el in window:
        mag = np.sqrt((el[0]*el[0] + el[1]*el[1] + el[2]*el[2]))
        magnitude.append(mag)
    
    return magnitude


def _compute_peak_length(window):

    # window_split = np.hsplit(np.asarray(window),3)

    # x_sq = 0
    # y_sq = 0
    # z_sq = 0

    # for x_el,y_el,z_el in zip(window_split[0],window_split[1],window_split[2]):
    #     for n in x_el:
    #         x_sq = x_sq + (n*n)
    #     for n in y_el:
    #         y_sq = y_sq + (n*n)
    #     for n in z_el:
    #         z_sq = z_sq + (n*n)

    magnitude = _compute_magnitude(window)

    peaks, _ = find_peaks(magnitude, prominence=1)

    return [len(peaks)]


def extract_features(window):
    """
    Here is where you will extract your features from the data over 
    the given window. We have given you an example of computing 
    the mean and appending it to the feature vector.
    
    """
    
    x = []
    feature_names = []

    x.append(_compute_mean_features(window))
    feature_names.append("x_mean")
    feature_names.append("y_mean")
    feature_names.append("z_mean")

    # TODO: call functions to compute other features. Append the features to x and the names of these features to feature_names

    x.append(_compute_std_features(window))
    feature_names.append("x_standard_deviation")
    feature_names.append("y_standard_deviation")
    feature_names.append("z_standard_deviation")

    x.append(_compute_peak_length(window))
    feature_names.append("magnitude peak length")

    x.append(_compute_dominant_frequency(window))
    feature_names.append("x_dominant_frequency")
    feature_names.append("y_dominant_frequency")
    feature_names.append("z_dominant_frequency")

    feature_vector = np.concatenate(x, axis=0) # convert the list of features to a single 1-dimensional vector
    return feature_names, feature_vector