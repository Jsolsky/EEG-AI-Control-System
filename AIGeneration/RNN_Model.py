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

# Local Functions
from PreProcessingandDataLoading.findDataFiles import findDataFiles
from PreProcessingandDataLoading.preProcessing import Preprocessing

################################################################################
# Creating logging
################################################################################
# Create the output directory if it doesn't exist
output_directory = './tmp_out/MNEDataset/log'
os.makedirs(output_directory, exist_ok=True)

# Configuring the logger
logger = logging.getLogger('MNEDataset')
logger.setLevel(logging.DEBUG)

# Setting up the console handler
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)

# Setting up the file handler
timeticks = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
log_file = os.path.join(output_directory, f'{timeticks}.log')
file_handler = logging.FileHandler(log_file)
logger.addHandler(file_handler)

################################################################################
# Seeding to ensure AI generation is deterministic
################################################################################
def seed_everything(seed):
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

seed_everything(42)

################################################################################
# Customise Trainer
################################################################################
class MyClassificationTrainer(ClassificationTrainer):
    def log(self, *args, **kwargs):
        if self.is_main:
            logger.info(*args, **kwargs)

################################################################################
# Creating list of data sets to use in training.
################################################################################
numSubjects = 109
runNum = ["R06", "R07", "R10"]

data_files = findDataFiles(numSubjects, runNum)

# print(data_files)

################################################################################
# Preprocessing Data
################################################################################
preProcessedDataset = Preprocessing(data_files)

################################################################################
# Training AI
################################################################################
# Determining number of splits for k fold training
k_fold = KFold(n_splits=5, split_path='./tmp_out/MNEDataset/split')

# Defining model
for i, (train_dataset, val_dataset) in enumerate(k_fold.split(preProcessedDataset)):
    # Initialize the model
    model = TSCeption(num_electrodes=64,
                      num_classes=2,
                      num_T=15,
                      num_S=15,
                      in_channels=1,
                      hid_channels=32,
                      sampling_rate=160,
                      dropout=0.5)

    # Initialize the trainer and use the 0-th GPU for training, or set device_ids=[] to use CPU
    trainer = MyClassificationTrainer(model=model,
                                      lr=1e-4,
                                      weight_decay=1e-4,
                                      device_ids=[0])

    # Initialize several batches of training samples and test samples
    train_loader = DataLoader(train_dataset,
                              # batch_size=len(train_dataset),
                              shuffle=True,
                              num_workers=4)
    val_loader = DataLoader(val_dataset,
                            # batch_size=len(val_dataset),
                            shuffle=False,
                            num_workers=4)

# Starting training
    # Do 50 rounds of training
    trainer.fit(train_loader, val_loader, num_epochs=50)
    trainer.test(val_loader)
    trainer.save_state_dict(f'./tmp_out/MNEDataset/weight/{i}.pth')
