import logging
import os
import random
import time

import mne
import numpy as np
import torch
from torch.utils.data.dataloader import DataLoader

from torcheeg import transforms
from torcheeg.datasets import MNEDataset
from torcheeg.model_selection import KFold
from torcheeg.models import TSCeption
from torcheeg.trainers import ClassificationTrainer

def Preprocessing(data_files):
    metadata_list = []

    for file_path in data_files:
        subject_id = os.path.basename(os.path.dirname(file_path))
        run_id = os.path.splitext(os.path.basename(file_path))[0][4:]
        metadata_list.append({
            'subject': subject_id,
            'run': run_id
        })

    # print(metadata_list)

    epochs_list = []

    for file_path in data_files:
        #Loading Data
        raw = mne.io.read_raw_edf(file_path, preload=True, stim_channel='auto')
        mne.datasets.eegbci.standardize(raw)

        montage = mne.channels.make_standard_montage('standard_1005')
        raw.set_montage(montage)

        # Filtering Data
        raw.filter(7., 30., fir_design='firwin', skip_by_annotation='edge')
        events, _ = mne.events_from_annotations(raw, event_id=dict(T1=2, T2=3))
        picks = mne.pick_types(raw.info,
                               meg=False,
                               eeg=True,
                               stim=False,
                               eog=False,
                               exclude='bads')
        # init Epochs with raw EEG signals and corresponding event annotations. Here, tmin is set to -1., and tmax is set to 4.0, to avoid classification of evoked responses by using epochs that start 1s after cue onset.
        epochs_list.append(
            mne.Epochs(raw,
                       events,
                       dict(hands=2, feet=3),
                       tmin=-1.,
                       tmax=4.0,
                       proj=True,
                       picks=picks))

    preProcessedDataset = MNEDataset(epochs_list=epochs_list,
                                     metadata_list=metadata_list,
                                     chunk_size=160,
                                     overlap=80,
                                     io_path='./tmp_out/MNEDataset/physionet',
                                     offline_transform=transforms.Compose(
                                         [transforms.MeanStdNormalize(),
                                          transforms.To2d()]),
                                     online_transform=transforms.ToTensor(),
                                     label_transform=transforms.Compose([
                                         transforms.Select('event'),
                                         transforms.Lambda(lambda x: x - 2)
                                     ]),
                                     num_worker=2)
    return preProcessedDataset
