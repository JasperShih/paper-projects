# -*- coding: utf8 -*-
__author__ = 'Jasper'

import math
import copy
import random
import scipy.misc as misc
import os
import cPickle as Pickle
import xlsxwriter


class Embed():
    def __init__(self, image, threshold, t_star):
        self.image = image
        self.threshold = threshold
        self.t_star = t_star

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


    def hide(self):
        # Throughout_image_by_chessboard
        for row in xrange(0, len(self.image)):
            # If current row is odd, first_of_row = 0
            # If current row is even, first_of_row = 1
            first_of_row = row % 2
            for col in xrange(first_of_row,
                              len(self.image[0]), 2):
                # We filtered elements which are None
                filtered_4pixels = filter(None, self.get_4adjacent_pixels(row, col))
                filtered_4pixels_avg = self.avg_reduce(lambda a, b: a + b, filtered_4pixels)

                complexity = max(
                    map(lambda a: a - filtered_4pixels_avg, filtered_4pixels)
                )

                if complexity < self.threshold:
                    # hiding


def main(image, threshold, t_star):
    # 1020 is max THRESHOLD, -1 TODO
    img_misc = misc.imread(image)
    img = img_misc.tolist()

    embed_obj = Embed(img, threshold, t_star)
    embed_obj.hide()


if __name__ == '__main__':
    main("C:\\Users\\Jasper\\Desktop\\image\\invest.bmp",
         5, 2)











