# EEG AI Control System

## Adding data to your local repo
- Download and extract the zip from [Dataset](https://physionet.org/content/eegmmidb/1.0.0/)
- Add the contents of the "files" folder in the downloaded dataset into the contents into the "files" directory of the EEG-AI-CONTROL-SYSTEM repository

## Installing python prerequites
- Make sure that you have anaconda [installed](https://www.anaconda.com/products/distribution)
- To install MNE using their [guide](https://mne.tools/stable/install/index.html) or run the following within your terminal:

```
conda install --channel=conda-forge --name=base mamba
mamba create --override-channels --channel=conda-forge --name=mne mne
```