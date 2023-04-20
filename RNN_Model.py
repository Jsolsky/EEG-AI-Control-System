""""
from pyeeglab import *


def EEG_clean():
    dataset = TUHEEGAbnormalDataset()
    preprocessing = Pipeline([
        CommonChannelSet(),
        LowestFrequency(),
        ToDataframe(),
        MinMaxCentralizedNormalization(),
        DynamicWindow(8),
        ToNumpy()
    ])
    dataset = dataset.set_pipeline(preprocessing).load()
    data, labels = dataset['data'], dataset['labels']
"""
from scipy.io import loadmat
annots = loadmat(r'C:\Users\ingra\OneDrive\Desktop\Professional_Studio_A\EEG-AI-Control-System\EEG_Data\B01T.mat')
print(annots)