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

    def get_4adjacent_pixels(self, row, col):
        # Top, left, right, bot
        return [
            self.image[row - 1][col] if row - 1 >= 0 else None,
            self.image[row][col - 1] if col - 1 >= 0 else None,
            self.image[row][col + 1] if col + 1 < len(self.image[0]) else None,
            self.image[row + 1][col] if row + 1 < len(self.image) else None
        ]

    # reduce then compute avg
    def avg_reduce(self, func, seq):
        first_element = seq[0]
        count = 1
        for next_element in seq[1:]:
            first_element = func(first_element, next_element)
            count += 1
        return first_element / count

    def undifference_expand(self, difference_value):
        two_t_star = 2 * self.t_star
        if -two_t_star <= difference_value <= (two_t_star + 1):
            watermark_bit = str(difference_value % 2)
            original_value = difference_value / 2
        elif difference_value <= -(two_t_star + 1):  # dL-T*
            watermark_bit = '*'
            original_value = difference_value + self.t_star
        elif (two_t_star + 2) <= difference_value:  # T*<dL
            watermark_bit = '*'
            original_value = difference_value - self.t_star - 1

        return watermark_bit, original_value

    def extract(self):
        watermark_bit_string = ""

        # Backwardly throughout_image_by_chessboard
        # White part first TODO
        for row in reversed(xrange(0, len(self.image))):
            # If current row is odd, first_of_row = 1
            # If current row is even, first_of_row = 0
            # first_of_row = (row+1) % 2 TODO
            first_of_row = row % 2
            for col in reversed(
                    xrange(first_of_row, len(self.image[0]), 2)):
                # We filtered elements which are None
                filtered_4pixels = filter(None, self.get_4adjacent_pixels(row, col))
                filtered_4pixels_avg = self.avg_reduce(lambda a, b: a + b, filtered_4pixels)

                complexity = max(
                    map(lambda a: a - filtered_4pixels_avg, filtered_4pixels)
                )

                if complexity < self.threshold:
                    # undifference_expand left_difference
                    overflow_flag = 0
                    # TODO
                    """
                    for pair in self.OVER_OR_UNDER_FLOW:
                        if pair[0] == central_row and pair[1] == (central_col - 1):
                            overflow_flag = 1
                            block_watermark += '*'
                            break
                    """
                    if overflow_flag is 0:
                        watermark_bit, original_value = self.undifference_expand(
                            self.image[row][col] - filtered_4pixels_avg)
                        watermark_bit_string += watermark_bit
                        self.image[row][col] = original_value + filtered_4pixels_avg  # TODO

        ori_image_misc = misc.imread("C:\\Users\\Jasper\\Desktop\\image\\invest.bmp")
        ori_image = ori_image_misc.tolist()

        if ori_image == self.image:
            print "good"

        #print ori_image
        #print self.image

        # watermark_bit_string is reversed order
        for i in reversed(watermark_bit_string):
            print i,




def main(image_path):
    extract_obj = Recover(image_path)
    extract_obj.extract()


if __name__ == '__main__':
    main("C:\\Users\\Jasper\\Desktop\\Pps\\P4\\output\\Stego.bmp")











