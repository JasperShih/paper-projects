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

        data_file = file(u"output//stego.data", 'r')
        # [(row, col), (row, col), ......]
        self.random_seed, self.over_or_under_flow = Pickle.load(data_file)
        data_file.close()

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
        # Extracted watermark
        extracted_watermark_white = ""
        extracted_watermark_black = ""

        # Backwardly throughout_image_by_chessboard
        # White part first
        for row in reversed(xrange(0, len(self.image))):
            # If current row is odd, first_of_row = 1
            # If current row is even, first_of_row = 0
            first_of_row = (row+1) % 2

            for col in reversed(
                    xrange(first_of_row, len(self.image[0]), 2)):
                # We filtered elements which are None
                filtered_4pixels = filter(None, self.get_4adjacent_pixels(row, col))
                filtered_4pixels_avg = self.avg_reduce(lambda a, b: a + b, filtered_4pixels)

                complexity = max(
                    map(lambda a: a - filtered_4pixels_avg, filtered_4pixels)
                )

                if complexity < self.threshold:
                    # un_difference_expand
                    # If current processing pixel belong overflow pixel, recover it and skip it.
                    # Else, un_difference_expand
                    for pair in self.over_or_under_flow:
                        if pair[0] == row and pair[1] == col:
                            watermark_bit = '*'
                            break
                    else:
                        watermark_bit, original_value = self.undifference_expand(
                            self.image[row][col] - filtered_4pixels_avg)
                        self.image[row][col] = original_value + filtered_4pixels_avg
                extracted_watermark_white += watermark_bit
        # extracted_watermark is reversed order
        extracted_watermark_white = extracted_watermark_white[::-1]


        # Black part
        for row in reversed(xrange(0, len(self.image))):
            # If current row is odd, first_of_row = 0
            # If current row is even, first_of_row = 1
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
                    # un_difference_expand
                    # If current processing pixel belong overflow pixel, recover it and skip it.
                    # Else, un_difference_expand
                    for pair in self.over_or_under_flow:
                        if pair[0] == row and pair[1] == col:
                            watermark_bit = '*'
                            break
                    else:
                        watermark_bit, original_value = self.undifference_expand(
                            self.image[row][col] - filtered_4pixels_avg)
                        self.image[row][col] = original_value + filtered_4pixels_avg
                extracted_watermark_black += watermark_bit
        # extracted_watermark is reversed order
        extracted_watermark_black = extracted_watermark_black[::-1]

        extracted_watermark = extracted_watermark_black + extracted_watermark_white

        # =================================== Result ========================================
        ori_image_misc = misc.imread("C:\\Users\\Jasper\\Desktop\\image\\Peppers.bmp")
        ori_image = ori_image_misc.tolist()
        if ori_image == self.image:
            print "Same"
            # print ori_image
            # print self.image

        random.seed(self.random_seed)
        regenerated_watermark = ""
        for i in xrange(
                                len(self.image) * len(self.image[0])
        ):
            regenerated_watermark += str(random.randint(0, 1))

        for i in xrange(len(regenerated_watermark)):
            if extracted_watermark[i] == '*' or \
                            extracted_watermark[i] == regenerated_watermark[i]:
                pass
            else:
                print "GG"
                break
        else:
            print "Yes"


def main(image_path):
    extract_obj = Recover(image_path)
    extract_obj.extract()


if __name__ == '__main__':
    main("C:\\Users\\Jasper\\Desktop\\Pps\\P4\\output\\Stego.bmp")











