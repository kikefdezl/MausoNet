import os
from shutil import copyfile
from tqdm import tqdm
import numpy as np
import cv2


def get_image_arrays():
    # 0 = no_maus, 1 = maus
    mausonet_db_dir = '/media/kike/HDD/MULTIMEDIA/MausoNet_dataset'
    maus_dir = mausonet_db_dir + '/maus/'
    no_maus_dir = mausonet_db_dir + '/no_maus/'

    X, Y = [], []
    for file in tqdm(os.listdir(maus_dir)):
        image = cv2.imread(maus_dir + file)
        image = cv2.resize(image, (512, 512))

        X.append(image)
        Y.append(1)


    for file in tqdm(os.listdir(no_maus_dir)):
        image = cv2.imread(no_maus_dir + file)
        image = cv2.resize(image, (512, 512))

        X.append(image)
        Y.append(0)

    np.savetxt('X.csv', X, delimiter=',')
    np.savetxt('Y.csv', Y, delimiter=',')

def split_into_trainval_test():

    test_split = 0.1

    mausonet_db_dir = '/media/kike/HDD/MULTIMEDIA/MausoNet_dataset'
    maus_dir = mausonet_db_dir + '/maus/'
    no_maus_dir = mausonet_db_dir + '/no_maus/'
    maus_trainval_dir = mausonet_db_dir + '/split/trainval/maus/'
    no_maus_trainval_dir = mausonet_db_dir + '/split/trainval/no_maus/'
    maus_test_dir = mausonet_db_dir + '/split/test/maus/'
    no_maus_test_dir = mausonet_db_dir + '/split/test/no_maus/'

    all_maus_images = os.listdir(maus_dir)
    all_no_maus_images = os.listdir(no_maus_dir)

    for index, image in tqdm(enumerate(all_maus_images)):
        source_path = maus_dir + image
        if index < (len(all_maus_images)*test_split):
            destination_path = maus_test_dir + image
        else:
            destination_path = maus_trainval_dir + image
        copyfile(source_path, destination_path)

    print(f"Split {index} maus images")

    for index, image in tqdm(enumerate(all_no_maus_images)):
        source_path = no_maus_dir + image
        if index < (len(all_no_maus_images) * test_split):
            destination_path = no_maus_test_dir + image
        else:
            destination_path = no_maus_trainval_dir + image
        copyfile(source_path, destination_path)

    print(f"Split {index} no_maus images")


if __name__ == "__main__":
    split_into_trainval_test()