# -*- coding: utf8 -*-
__author__ = 'Jasper'

import numpy as np
import math
import copy
import random
import scipy.misc as misc
import os
import cPickle as Pickle
import xlsxwriter

#C:\\Users\\Jasper\\Desktop\\Pps\\P4\\output\\UnembeddableBlockLena,14,0.bmp
#C:\\Users\\Jasper\\Desktop\\output\\unembeddableBlockLenaP1.bmp
image_path = "C:\\Users\\Jasper\\Desktop\\output\\unembeddableBlockLenaP2.bmp"
image_misc = misc.imread(image_path)


def black_block_count(image, block_size):
        count = 0
        for row in xrange(0, len(image) - block_size + 1, block_size):
            for col in xrange(0, len(image[0]) - block_size + 1, block_size):
                if image[row][col] == 0:
                    count += 1
        return (16384-count)/16384.0

print black_block_count(image_misc, 4)








