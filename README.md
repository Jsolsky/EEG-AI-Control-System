# EEG AI Control System

## Adding Raw Data to project
The [Dataset](https://physionet.org/content/eegmmidb/1.0.0/) is should be placed within the project's directories as such:
```
- EEG-AI-CONTROL-SYSTEM 
   - AIGeneration
      - RNN_Model.py
      - PreProcessingandDataLoading
      - rawData <-- Data directory
        - S001
        - S002
        - ***
        - S109
```

## Installing Python prerequisites
- To install MNE using their [guide](https://mne.tools/stable/install/index.html) or by running the following within your terminal:
```
pip install mne
```
- Pytorch should be installed using pip by following their [guide](https://pytorch.org/)
- TORCHEEG can be installed as follows:
```
pip install torcheeg 
```
