import os
import mne
from torcheeg.datasets import MNEDataset

# INPUTS: 
# A list of the subject id's (e.g. [1,2,3,4] OR list(range(1,110)) )
#starts at 1

# OUTPTUS:
# dataset - MNE dataset object from torchEEG

def load_data(subject_id_list):
    filename_raw = "files/S" 

    # the code below can be put into a loop itterating on subject = range(1, 109)
    "001/S001R"
    epochs_list = []


    for subject_id in subject_id_list:
        metadata_list = [{
            'subject': subject_id,
            'run': run_id
        } for subject_id in subject_id_list
                        for run_id in range(1,15)]


        for i in range(1, 15):
        # for i in [3]:
            filename_EEG = filename_raw + "%03d" % (subject_id,) + "/S" + "%03d" % (subject_id,) + "R" + "%02d" % (i,) + ".edf"
            raw_EEG_data = mne.io.read_raw_edf(filename_EEG, preload = True)

            # modified code from github
            # This step can be done before or after event extraction
            action_dict = dict()

            if i in [3, 7, 11]:
                for index, an in enumerate(raw_EEG_data.annotations.description):
                    # an = annotation
                    if an == "T0":
                        raw_EEG_data.annotations.description[index] = "B"
                    if an == "T1":
                        raw_EEG_data.annotations.description[index] = "L"
                    if an == "T2":
                        raw_EEG_data.annotations.description[index] = "R"
                    
                    action_dict = dict(B=1, L=2, R=3) # this encodes the annotation for epcohs

            elif i in [4, 8, 12]:
                for index, an in enumerate(raw_EEG_data.annotations.description):
                    # an = annotation
                    if an == "T0":
                        raw_EEG_data.annotations.description[index] = "B"
                    if an == "T1":
                        raw_EEG_data.annotations.description[index] = "IL"
                    if an == "T2":
                        raw_EEG_data.annotations.description[index] = "IR"
                    
                    action_dict = dict(B=1, IL=2, IR=3) # this encodes the annotation for epcohs
            
            elif i in [5, 9, 13]:
                for index, an in enumerate(raw_EEG_data.annotations.description):
                    if an == "T0":
                        raw_EEG_data.annotations.description[index] = "B"
                    if an == "T1":
                        raw_EEG_data.annotations.description[index] = "LR"
                    if an == "T2":
                        raw_EEG_data.annotations.description[index] = "F"
                        # print(raw_EEG_data.annotations.description[index])
                    
                    action_dict = dict(B=1, LR=2, F=3) # this encodes the annotation for epcohs
        
            elif i in [6, 10, 14]:
                for index, an in enumerate(raw_EEG_data.annotations.description):
                    if an == "T0":
                        raw_EEG_data.annotations.description[index] = "B"
                    if an == "T1":
                        raw_EEG_data.annotations.description[index] = "ILR"
                    if an == "T2":
                        raw_EEG_data.annotations.description[index] = "IF"
                        # print(raw_EEG_data.annotations.description[index])

                    action_dict = dict(B=1, ILR=2, IF=3) # this encodes the annotation for epcohs

            else: 
                for index, an in enumerate(raw_EEG_data.annotations.description):
                    if an == "T0":
                        raw_EEG_data.annotations.description[index] = "B"

                    action_dict = dict(B=1) # this encodes the annotation for epcohs
            
            raw_EEG_events, summary = mne.events_from_annotations(raw_EEG_data)
            
            raw_EEG_epochs = mne.Epochs(raw_EEG_data, raw_EEG_events, action_dict, tmin=-1., tmax=4.0, preload=True)
            # can use mne.Epochs(picks = Channels) to specify which channels to use
            epochs_list.append(raw_EEG_epochs)

    dataset = MNEDataset(epochs_list = epochs_list, metadata_list = metadata_list, io_mode='pickle', num_worker=1)

    return dataset