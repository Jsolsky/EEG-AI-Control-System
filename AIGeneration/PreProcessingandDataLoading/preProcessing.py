# import logging
# import os
# import random
# import time

# import mne
# import numpy as np
# import torch
# from torch.utils.data.dataloader import DataLoader

# from torcheeg import transforms
# from torcheeg.datasets import MNEDataset
# from torcheeg.model_selection import KFold
# from torcheeg.models import TSCeption
# from torcheeg.trainers import ClassificationTrainer

# NumSubjects = 109 # The Max Number of subjects is 109
# metadata_list = [{
#     'subject': subject_id,
#     'run': run_id
# } for subject_id in range(1, NumSubjects)
#                  for run_id in [6, 10, 14]]  # motor imagery: hands vs feet

# epochs_list = []
# for metadata in metadata_list:
#     edf_path = os.path.join(metadata['subject'],
#                                     metadata['run'],)
#                                       
#     raw = mne.io.read_raw_edf(physionet_path, preload=True, stim_channel='auto')
#     mne.datasets.eegbci.standardize(raw)

#     montage = mne.channels.make_standard_montage('standard_1005')
#     raw.set_montage(montage)

#     raw.filter(7., 30., fir_design='firwin', skip_by_annotation='edge')
#     events, _ = mne.events_from_annotations(raw, event_id=dict(T1=2, T2=3))
#     picks = mne.pick_types(raw.info,
#                            meg=False,
#                            eeg=True,
#                            stim=False,
#                            eog=False,
#                            exclude='bads')
#     # init Epochs with raw EEG signals and corresponding event annotations. Here, tmin is set to -1., and tmax is set to 4.0, to avoid classification of evoked responses by using epochs that start 1s after cue onset.
#     epochs_list.append(
#         mne.Epochs(raw,
#                    events,
#                    dict(hands=2, feet=3),
#                    tmin=-1.,
#                    tmax=4.0,
#                    proj=True,
#                    picks=picks))

# ###############################################################################
# # Convert :obj:`mne.Epochs` into MNEDataset
# # -----------------------------------------
# # We use MNEDataset to window the Epochs. Here, we set the window size to 160 (1-second long) and the overlap to 80 to segment the EEG signal corresponding to each event. The corresponding information in :obj:`metadata_list` will be assigned to the corresponding window. At the same time, the window also includes the start position of the window :obj:`start_at`, the end position :obj:`start_at`, the epoch index :obj:`trial_id` and the corresponding event type :obj:`event`, which can be used and transformed as label.
# #
# dataset = MNEDataset(epochs_list=epochs_list,
#                      metadata_list=metadata_list,
#                      chunk_size=160,
#                      overlap=80,
#                      io_path='./tmp_out/examples_mne_dataset/physionet',
#                      offline_transform=transforms.Compose(
#                          [transforms.MeanStdNormalize(),
#                           transforms.To2d()]),
#                      online_transform=transforms.ToTensor(),
#                      label_transform=transforms.Compose([
#                          transforms.Select('event'),
#                          transforms.Lambda(lambda x: x - 2)
#                      ]),
#                      num_worker=2)
