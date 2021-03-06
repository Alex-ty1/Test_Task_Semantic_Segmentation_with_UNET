#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import sys
import random
import warnings

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from tqdm import tqdm
from itertools import chain
from skimage.io import imread, imshow, imread_collection, concatenate_images
from skimage.transform import resize
from skimage.morphology import label

IMG_WIDTH = 128
IMG_HEIGHT = 128
IMG_CHANNELS = 3


# In[ ]:


TRAIN_PATH ='train_images' 
TEST_PATH ='test_images' # image path


# In[ ]:


train_ids = next(os.walk(TRAIN_PATH))[1]
test_ids = next(os.walk(TEST_PATH))[1]


# In[ ]:


def load_data(IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS):
    X_train = np.zeros((len(train_ids), IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS), dtype=np.uint8)
    Y_train = np.zeros((len(train_ids), IMG_HEIGHT, IMG_WIDTH, 1), dtype=np.bool)
    print('Getting and resizing train images and masks ... ')
    sys.stdout.flush()
    for n, id_ in tqdm(enumerate(train_ids), total=len(train_ids)):
        path = TRAIN_PATH +'/' + id_
        img = imread(path + '/images/' + id_ + '.png')[:,:,:IMG_CHANNELS]
        img = resize(img, (IMG_HEIGHT, IMG_WIDTH), mode='constant', preserve_range=True)
        X_train[n] = img
        mask = np.zeros((IMG_HEIGHT, IMG_WIDTH, 1), dtype=np.bool)
        for mask_file in next(os.walk(path + '/masks/'))[2]:
            mask_ = imread(path + '/masks/' + mask_file)
            mask_ = np.expand_dims(resize(mask_, (IMG_HEIGHT, IMG_WIDTH), mode='constant', 
                                      preserve_range=True), axis=-1)
            mask = np.maximum(mask, mask_)
        Y_train[n] = mask

    # Get and resize test images
    X_test = np.zeros((len(test_ids), IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS), dtype=np.uint8)
    sizes_test = []
    print('Getting and resizing test images ... ')
    sys.stdout.flush()
    for n, id_ in tqdm(enumerate(test_ids), total=len(test_ids)):
        path = TEST_PATH  + '/' + id_
        img = imread(path + '/images/' + id_ + '.png')[:,:,:IMG_CHANNELS]
        sizes_test.append([img.shape[0], img.shape[1]])
        img = resize(img, (IMG_HEIGHT, IMG_WIDTH), mode='constant', preserve_range=True)
        X_test[n] = img

    print('Done!')
    return X_train, Y_train, X_test


# In[ ]:


def plot_example(X_train, Y_train):
    ix = random.randint(0, len(X_train))
    has_mask = Y_train[ix].max() > 0 # salt indicator

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (20, 15))

    ax1.imshow(X_train[ix, ..., 0], cmap = 'seismic', interpolation = 'bilinear')
    if has_mask: # if salt
    # draw a boundary(contour) in the original image separating salt and non-salt areas
        ax1.contour(Y_train[ix].squeeze(), colors = 'k', linewidths = 5, levels = [0.5])
    ax1.set_title('Seismic')

    ax2.imshow(Y_train[ix].squeeze(), cmap = 'gray', interpolation = 'bilinear')
    ax2.set_title('Salt')

