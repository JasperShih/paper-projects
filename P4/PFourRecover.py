# -*- coding: utf8 -*-
__author__ = 'Jasper'

import math
import copy
import random
import scipy.misc as misc
import os
import cPickle as Pickle
import xlsxwriter


class Recover():
    def __init__(self, image_path):
        self.image_misc = misc.imread(image_path)
        self.image = self.image_misc.tolist()
        self.threshold = 255
        self.t_star = 255


    def extract(self):
        random.seed(10)  # TODO

        # Backwardly throughout_image_by_chessboard
        # Black part first
        seq_buf = []
        for row in xrange(0, len(self.image)):
            # If current row is odd, first_of_row = 1
            # If current row is even, first_of_row = 0
            first_of_row = (row+1) % 2
            for col in xrange(first_of_row,
                              len(self.image[0]), 2):
                seq_buf += [row, col]
                # We filtered elements which are None
                filtered_4pixels = filter(None, self.get_4adjacent_pixels(row, col))
                filtered_4pixels_avg = self.avg_reduce(lambda a, b: a + b, filtered_4pixels)

                complexity = max(
                    map(lambda a: a - filtered_4pixels_avg, filtered_4pixels)
                )
                random_bit = random.randint(0, 1)
                embeddable = 0
                if complexity < self.threshold:
                    difference_prime, embeddable = \
                        self.difference_expand(self.image[row][col] - filtered_4pixels_avg,
                                               random_bit, embeddable)

                    modified_value = difference_prime + filtered_4pixels_avg
                    if (modified_value > 255) or (modified_value < 0):
                        self.over_or_under_flow.append((row, col))
                        self.over_or_under_flow_bits += 1
                        embeddable = 0
                    else:
                        self.image[row][col] = modified_value

                    if embeddable:
                        un_embeddable_image[row][col] = 255



def main(image_path):
    extract_obj = Recover(image_path)
    extract_obj.extract()


if __name__ == '__main__':
    main("C:\\Users\\Jasper\\Desktop\\Pps\\P4\\output\\Stego.bmp")











