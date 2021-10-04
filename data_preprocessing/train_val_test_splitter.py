import os
import shutil
from random import shuffle

def main():
    dataset_dir = '/media/kike/HDD/MULTIMEDIA/MausoNet_dataset/'

    all_filenames = []
    for filename in os.listdir(dataset_dir+'maus'):
        all_filenames.append(dataset_dir+'maus/'+filename)

    for filename in os.listdir(dataset_dir+'no_maus'):
        all_filenames.append(dataset_dir+'no_maus/'+filename)

    shuffle(all_filenames)


if __name__ == "__main__":
    main()